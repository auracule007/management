
from django.db.models import OuterRef, Q, Subquery
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import filters, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from subscriptions.emails import send_subscription_confirmation
from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer
from utils import create_calendar

from utils.calendars import create_google_calendar_event
from utils.flutter import initiate_payment
from utils.permissions import SubscriptionPermission
from . models import *
from . permissions import *
from . serializers import *
from djoser.views import UserViewSet as DjoserUserViewSet
from analytics.serializers import CourseRatingSerializer
from . pagination import *

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().select_related("profile")
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ("username", "first_name", "last_name", "email")
    search_fields = ("username", "first_name", "last_name", "email")

    def get_permission_class(self):
        if self.request.method in ["DELETE"]:
            return [permissions.IsAdminUser()]
        return permissions.AllowAny()


# Category viewset
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.order_by("name").prefetch_related('courses_set').all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name"]

class ContactViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = Contact.objects.all().order_by("name")
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]

# Courses viewset
class CoursesViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["category__name", "name", "instructor", "price"]
    pagination_class = CoursesPagination

    def get_permissions(self):
        if self.request.method in ["POST", "PATCH", "PUT", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return Courses.objects.filter(category_id=self.kwargs.get('category_pk')).order_by("name")
        

# create course viewset
class CreateCoursesViewSet(ModelViewSet):
    queryset = Courses.objects.all().order_by("name")
    serializer_class = CreateCourseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializers = CreateCourseSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(instructor=request.user.instructor)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.error, status=status.HTTP_400_BAD_REQUEST)


class CourseRequirementViewSet(ModelViewSet):
    serializer_class = CourseRequirementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        return CourseRequirement.objects.filter(course_id=self.kwargs.get('courses_pk')).select_related('course')

# class ModuleViewSet(ModelViewSet):
#     serializer_class = ModuleSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     def get_queryset(self):
#         return Module.objects.filter(course_id=self.kwargs.get('courses_pk')).select_related('course')
    
from decimal import Decimal
# enroll for a course viewset
class EnrollmentViewSet(ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(
            student_id = self.request.user.student.id
        ).select_related("courses", "student")

    def create(self, request):
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            # Get the course and its price
            course_id = serializer.validated_data['courses_id']
            course = Courses.objects.get(id=course_id)
            course_price = course.price

            # Calculate the new price based on the interval
            interval = serializer.validated_data['interval']
            if interval == 'Monthly':
                new_price = course_price * Decimal('4')  # 4 weeks in a month
            elif interval == 'Yearly':
                new_price = course_price * Decimal('52')  # 52 weeks in a year
            elif interval == 'Weekly':
                new_price = course_price * Decimal('1')  # Price per week
            else:
                new_price = course_price
            serializer.validated_data['price'] = new_price
            enrollment = Enrollment.objects.create(
                student=request.user.student,
                courses_id=course_id,
                interval=interval,
                # date_enrolled=serializer.validated_data['date_enrolled']
            )
            return Response(EnrollmentSerializer(enrollment).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def payment(self, request, pk):
        enrollment = self.get_object()
        course = enrollment.courses
        course_price = course.price

        # Calculate the new price based on the interval
        interval = enrollment.interval
        if interval == 'Monthly':
            new_price = course_price * Decimal('4')  # 4 weeks in a month
        elif interval == 'Yearly':
            new_price = course_price * Decimal('52')  # 52 weeks in a year
        elif interval == 'Weekly':
            new_price = course_price * Decimal('1')  # Price per week
        else:
            new_price = course_price

        amount = new_price
        promotion_price = course.promotion_price
        if promotion_price is not None:
            amount = promotion_price

        email = request.user.email
        user_id = request.user.id
        first_name = request.user.first_name
        last_name = request.user.last_name
        phone = request.user.phone
        enrollment_id = enrollment.pk
        return initiate_payment(amount, email, enrollment_id, user_id, first_name, last_name, phone)


    @action(detail=False, methods=["POST"], url_name='confirm-payment', url_path='confirm-payment')
    def confirm_payment(self, request):
        enrollment_id = request.GET.get("enrollment_id")
        if not enrollment_id:
            return Response({"error": "Missing enrollment_id parameter"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            enrollment = get_object_or_404(Enrollment, id=enrollment_id)
        except Enrollment.DoesNotExist:
            return Response({"error": "Invalid enrollment_id"}, status=status.HTTP_400_BAD_REQUEST)
        subscribed = Subscription.objects.create(enrollment_id=enrollment.id,user_id=self.request.user.id)
        status = request.GET.get("status")
        transaction_id = request.GET.get("transaction_id")
        try:
            if status == 'successful':
                subscribed.pending_status = 'C'
            else: 
                subscribed.pending_status = 'F'
        except Exception as err:
            return Response({'error': err })
        subscribed.transaction_id=transaction_id
        subscribed.save()
        # email notification
        send_subscription_confirmation(enrollment_id)
        serializer = SubscriptionSerializer(subscribed)
        
        data = {
            "message": "payment was successful",
            "data": serializer.data
        }
        return Response(data)

    # @action(detail=False, methods=["POST"], url_name='confirm-payment', url_path='confirm-payment')
    # def confirm_payment(self, request):
    #     enrollment_id = request.GET.get("enrollment_id")
    #     if not enrollment_id:
    #         return Response({"error": "Missing enrollment_id parameter"}, status=status.HTTP_400_BAD_REQUEST)
    #     try:
    #         enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    #     except Enrollment.DoesNotExist:
    #         return Response({"error": "Invalid enrollment_id"}, status=status.HTTP_400_BAD_REQUEST)

    #     # Get the course and its price
    #     course = enrollment.courses
    #     course_price = course.price

    #     # Calculate the new price based on the interval
    #     interval = enrollment.interval
    #     if interval == 'Monthly':
    #         new_price = course_price * Decimal('4')  # 4 weeks in a month
    #     elif interval == 'Yearly':
    #         new_price = course_price * Decimal('52')  # 52 weeks in a year
    #     elif interval == 'Weekly':
    #         new_price = course_price * Decimal('1')  # Price per week
    #     else:
    #         new_price = course_price

    #     subscribed = Subscription.objects.create(enrollment_id=enrollment.id, user_id=self.request.user.id, price=new_price)
    #     status = request.GET.get("status")
    #     transaction_id = request.GET.get("transaction_id")
    #     try:
    #         if status == 'successful':
    #             subscribed.pending_status = 'C'
    #         else:
    #             subscribed.pending_status = 'F'
    #     except Exception as err:
    #         return Response({'error': err})
    #     subscribed.transaction_id = transaction_id
    #     subscribed.save()
    #     # email notification
    #     send_subscription_confirmation(enrollment_id)
    #     serializer = SubscriptionSerializer(subscribed)

    #     data = {
    #         "message": "payment was successful",
    #         "data": serializer.data
    #     }
    #     return Response(data)

  
    # @action(detail=True, methods=['POST'])
    # def payment(self, request, pk):
    #     enrollment = self.get_object()
    #     course = enrollment.courses
    #     course_price = course.price

    #     # Calculate the new price based on the interval
    #     interval = enrollment.interval
    #     if interval == 'Monthly':
    #         new_price = course_price * Decimal('4')  # 4 weeks in a month
    #     elif interval == 'Yearly':
    #         new_price = course_price * Decimal('52')  # 52 weeks in a year
    #     elif interval == 'Weekly':
    #         new_price = course_price * Decimal('1')  # Price per week
    #     else:
    #         new_price = course_price

    #     # Update the course price in the database
    #     course.price = new_price
    #     course.save()

    #     amount = new_price
    #     promotion_price = course.promotion_price
    #     if promotion_price is not None:
    #         amount = promotion_price
    #     email = request.user.email
    #     user_id = request.user.id
    #     first_name = request.user.first_name
    #     last_name = request.user.last_name
    #     phone = request.user.phone
    #     enrollment_id = enrollment.pk
    #     return initiate_payment(amount, email, enrollment_id,user_id, first_name, last_name, phone)    
    
    # @action(detail=False, methods=["POST"], url_name='confirm-payment', url_path='confirm-payment')
    # def confirm_payment(self, request):
    #     enrollment_id = request.GET.get("enrollment_id")
    #     if not enrollment_id:
    #         return Response({"error": "Missing enrollment_id parameter"}, status=status.HTTP_400_BAD_REQUEST)
    #     try:
    #         enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    #     except Enrollment.DoesNotExist:
    #         return Response({"error": "Invalid enrollment_id"}, status=status.HTTP_400_BAD_REQUEST)

    #     # Get the course and its price
    #     course = enrollment.courses
    #     course_price = course.price

    #     # Calculate the new price based on the interval
    #     interval = enrollment.interval
    #     if interval == 'Monthly':
    #         new_price = course_price * Decimal('4')  # 4 weeks in a month
    #     elif interval == 'Yearly':
    #         new_price = course_price * Decimal('52')  # 52 weeks in a year
    #     elif interval == 'Weekly':
    #         new_price = course_price * Decimal('1')  # Price per week
    #     else:
    #         new_price = course_price

    #     subscribed = Subscription.objects.create(enrollment_id=enrollment.id, user_id=self.request.user.id, price=new_price)
    #     status = request.GET.get("status")
    #     transaction_id = request.GET.get("transaction_id")
    #     try:
    #         if status == 'successful':
    #             subscribed.pending_status = 'C'
    #         else: 
    #             subscribed.pending_status = 'F'
    #     except Exception as err:
    #         return Response({'error': err })
    #     subscribed.transaction_id = transaction_id
    #     subscribed.save()
    #     # email notification
    #     send_subscription_confirmation(enrollment_id)
    #     serializer = SubscriptionSerializer(subscribed)
        
    #     data = {
    #         "message": "payment was successful",
    #         "data": serializer.data
    #     }
    #     return Response(data)
    
    # def create(self, request):
    #     serializers = EnrollmentSerializer(data=request.data)
    #     if serializers.is_valid():
    #         serializers.save(student=request.user.student)
    #         return Response(serializers.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=True, methods=['POST'])
    # def payment(self, request, pk):
    #     enrollment = self.get_object()
    #     amount = enrollment.courses.price
    #     promotion_price = enrollment.courses.promotion_price
    #     if promotion_price is not None:
    #         amount = promotion_price
    #     email = request.user.email
    #     user_id = request.user.id
    #     first_name = request.user.first_name
    #     last_name = request.user.last_name
    #     phone = request.user.phone
    #     enrollment_id = enrollment.pk
    #     return initiate_payment(amount, email, enrollment_id,user_id, first_name, last_name, phone)
    
    # @action(detail=False, methods=["POST"], url_name='confirm-payment', url_path='confirm-payment')
    # def confirm_payment(self, request):
    #     enrollment_id = request.GET.get("enrollment_id")
    #     if not enrollment_id:
    #         return Response({"error": "Missing enrollment_id parameter"}, status=status.HTTP_400_BAD_REQUEST)
    #     try:
    #         enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    #     except Enrollment.DoesNotExist:
    #         return Response({"error": "Invalid enrollment_id"}, status=status.HTTP_400_BAD_REQUEST)
    #     subscribed = Subscription.objects.create(enrollment_id=enrollment.id,user_id=self.request.user.id)
    #     status = request.GET.get("status")
    #     transaction_id = request.GET.get("transaction_id")
    #     try:
    #         if status == 'successful':
    #             subscribed.pending_status = 'C'
    #         else: 
    #             subscribed.pending_status = 'F'
    #     except Exception as err:
    #         return Response({'error': err })
    #     subscribed.transaction_id=transaction_id
    #     subscribed.save()
    #     # email notification
    #     send_subscription_confirmation(enrollment_id)
    #     serializer = SubscriptionSerializer(subscribed)
        
    #     data = {
    #         "message": "payment was successful",
    #         "data": serializer.data
    #     }
    #     return Response(data)


    # @action(detail=False, methods=["POST"], url_name='confirm-payment', url_path='confirm-payment')
    # def confirm_payment(self, request):
    #     enrollment_id = request.GET.get("enrollment_id")
    #     if not enrollment_id:
    #         return Response({"error": "Missing enrollment_id parameter"}, status=status.HTTP_400_BAD_REQUEST)
    #     try:
    #         enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    #     except Enrollment.DoesNotExist:
    #         return Response({"error": "Invalid enrollment_id"}, status=status.HTTP_400_BAD_REQUEST)
    #     subscribed = Subscription.objects.create(enrollment_id=enrollment.id,user_id=self.request.user.id)
    #     status = request.GET.get("status")
    #     transaction_id = request.GET.get("transaction_id")
    #     try:
    #         if status == 'successful':
    #             subscribed.pending_status = 'C'
    #         else: 
    #             subscribed.pending_status = 'F'
    #     except Exception as err:
    #         return Response({'error': err })
    #     subscribed.transaction_id=transaction_id
    #     subscribed.save()
    #     # email notification
    #     send_subscription_confirmation(enrollment_id)
    #     serializer = SubscriptionSerializer(subscribed)
        
    #     data = {
    #         "message": "payment was successful",
    #         "data": serializer.data
    #     }
    #     return Response(data)
    

class CertificateViewSet(ModelViewSet):
    http_method_names = ['get']
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CertificateSerializer
    def get_queryset(self):
        return Certificate.objects.filter(enrollment_id=self.kwargs.get('enrollment_pk'))
    

class ContentUploadViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete", "patch", "put"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,SubscriptionPermission]

    def get_queryset(self):
        queryset = ContentUpload.objects.filter(course_id=self.kwargs.get('courses_pk')).filter(course__is_started=True).select_related("user")
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetContentUploadSerializer
        return ContentUploadSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        content = request.data.get("content", None)
        content_title = request.data.get("content_title", None)
        content_description = request.data.get("content_description", None)
        if content:
            setattr(instance, "content", content)
        if content_title:
            setattr(instance, "content_title", content_title)
        if content_description:
            setattr(instance, "content_description", content_description)
        instance.save()
        serializer = ContentUploadSerializer(instance)
        return Response(serializer.data)


class ModuleViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = ModuleSerializer

    def get_queryset(self):
        queryset = Modules.objects.filter(course_id=self.kwargs.get('courses_pk')).select_related('course').prefetch_related('lessons')
        return queryset
    

    
# class ContentManagementViewSet(ModelViewSet):
#     http_method_names = ["get"]
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = GetContentManagementSerializer
#     def get_queryset(self):
#         queryset = (
#             ContentManagement.objects.filter(is_approved=True)
#             .filter(user_id=self.request.user)
#             .prefetch_related("content_uploads")
#         )
#         return queryset
#     def perform_create(self, serializer):
#         serializer.save(user_id=self.request.user)


# chat viewsets
class ChatMessageView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]

        messages = ChatMessage.object.filter(
            id__in=Subquery(
                User.objects.filter(
                    Q(sender__receiver=user_id)
                    | Q(receiver__sender=user_id)
                    .distinct()
                    .annotate(
                        last_msg=Subquery(
                            ChatMessage.objects.filter(
                                Q(sender=OuterRef("id"), receiver=user_id)
                                | Q(receiver=OuterRef("id"), sender=user_id)
                                .order_by("-id")[:1]
                                .values_list("id", flat=True)
                            )
                        )
                        .values_list("last_msg", flat=True)
                        .order_by("-id")
                    )
                )
            )
        ).order_by("-id")
        return messages


class GetAllMessagesView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        sender_id = self.kwargs["sender_id"]
        receiver_id = self.kwargs["receiver_id"]

        messages = ChatMessage.objects.filter(
            sender__in=[sender_id, receiver_id], receiver__in=[sender_id, receiver_id]
        )
        return messages


class SendMessageView(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]


class SearchUserView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_list(self, request, *args, **kwargs):
        username = self.kwargs.get("username")
        logged_in_user = self.request.user
        users = Profile.objects.filter(
            Q(user__username__icontains=username) | Q(full_name__icontains=username)
        ).exclude(user=logged_in_user)

        if not users.exists():
            return Response(
                {"detail": "No users found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


class QuestionBankViewSet(ModelViewSet):
    queryset = QuestionBank.objects.all().order_by("course__id")
    serializer_class = QuestionBankSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        serializers = QuestionBankSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(instructor=request.user.instructor)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.error, status=status.HTTP_400_BAD_REQUEST)


class QuestionViewSet(ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = (
        Question.objects.all()
        .order_by("question_bank__course__id")
        .prefetch_related("choice")
    )
    permission_classes = [permissions.IsAuthenticated]


class ChoicesViewSet(ModelViewSet):
    serializer_class = ChoicesSerializer
    queryset = Choice.objects.all().order_by("question__id")
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(question_id=self.kwargs.get("question_pk"))


class AssessmentViewSet(ModelViewSet):
    serializer_class = AssessmentSerialier

    def get_queryset(self):
        return

    def create(self, request):
        serializers = AssessmentSerialier(data=request.data)
        if serializers.is_valid():
            serializers.save(instructor=request.user.instructor)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.error, status=status.HTTP_400_BAD_REQUEST)


class GradeSubmissionView(generics.CreateAPIView):
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        assessment_id = request.data.get("assessment_id")
        answers_data = request.data.get("answers", [])

        try:
            submission = Submission.objects.get(
                user_id=user_id, assessment_id=assessment_id
            )
        except Submission.DoesNotExist:
            return Response(
                {"error": "Submission not found"}, status=status.HTTP_404_NOT_FOUND
            )

        answer_serializer = self.get_serializer(data=answers_data, many=True)
        answer_serializer.is_valid(raise_exception=True)

        answers = []
        for answer_data in answers_data:
            question_id = answer_data["question_id"]
            selected_choice_id = answer_data["selected_choice_id"]
            text = answer_data.get("text", "")
            try:
                question = Question.objects.get(pk=question_id)
                selected_choice = Choice.objects.get(pk=selected_choice_id)
            except (Question.DoesNotExist, Choice.DoesNotExist):
                return Response(
                    {"error": "Invalid question or choice ID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            is_correct = selected_choice.is_correct
            # Here you can implement your logic to calculate points based on correctness
            points = 1.0 if is_correct else 0.0

            answers.append(
                {
                    "question": question,
                    "text": text,
                    "selected_choice": selected_choice,
                    "is_correct": is_correct,
                    "points": points,
                }
            )

        # Save answers
        Answer.objects.filter(submission=submission).delete()  # Remove previous answers
        Answer.objects.bulk_create(
            [Answer(submission=submission, **answer) for answer in answers]
        )

        # Calculate total score
        total_score = sum(answer["points"] for answer in answers)

        # Update or create grading
        grading, created = Grading.objects.update_or_create(
            student=submission.user,
            assessment=submission.assessment,
            defaults={"score": total_score},
        )

        return Response(
            {"success": "Submission graded successfully", "score": grading.score},
            status=status.HTTP_201_CREATED,
        )


# Admin dashboard
class AdminDashboardViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = AdminUserSerializer
    permission_class = [permissions.IsAdminUser]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id).get(is_staff=True)

    def get_serializer_class(self):
        if self.action == "user_management":
            return UserSerializer
        return self.serializer_class

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated],
        url_path="user-managements",
        url_name="user-managements",
    )
    def user_management(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


# course event
class CourseEventViewset(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = CourseEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CourseEvent.objects.all()

    # def create(self, request, *args, **kwargs):         
        
    #     user = request.user
    #     data = request.data.copy()
    #     data["user"] = user.id
    #     try:
    #         is_existing = self.queryset.get(user=user)
    #         serializer = self.get_serializer(is_existing, data=data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except CourseEvent.DoesNotExist:
    #         serializer = self.get_serializer(data=data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save(user=user)
    #         create_calendar(serializer.data['event_text'])
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, *args, **kwargs):
    #     user = request.user
    #     data = request.data.copy()
    #     data["user"] = user.id
    #     try:
    #         instance = self.queryset.get(user=user)
    #         serializer = self.get_serializer(instance, data=data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

       
    #     # Create an event in Google Calendar and update the calendar_event_id field
    #     # user_id=self.request.user.id
    #     # course_event = serializer.save(user_id=self.request.user.id)
    #     # event_id = create_google_calendar_event(course_event)
    #     # course_event.calendar_event_id = event_id
    #     # course_event.save()


# course rating
class CourseRatingViewSet(ModelViewSet):
    serializer_class = GetCourseRatingSerializer
    queryset = CourseRating.objects.select_related('user','course')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return self.serializer_class
        return CourseRatingSerializer
