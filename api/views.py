from django.db import transaction
from django.db.models import OuterRef, Q, Subquery
from django.shortcuts import HttpResponse, render
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import *
from .permissions import *
from .serializers import *

# Create your views here.


# Category viewset
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer


# Courses viewset
class CoursesViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    search_fields = ["category__name", "name"]

    def get_queryset(self):
        queryset = Courses.objects.all().order_by("name")
        course_id = self.request.query_params.get("category_id")
        if course_id:
            queryset = Courses.objects.filter(
                category_id=self.request.query_params.get("category_id")
            )
        return queryset


# create course viewset
class CreateCoursesViewSet(ModelViewSet):
    queryset = Courses.objects.all().order_by("name")
    serializer_class = CreateCourseSerializer
    permission_classes = [IsStudentOrInstructor]

    def create(self, request):
        serializers = CreateCourseSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(instructor=request.user.instructor)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.error, status=status.HTTP_400_BAD_REQUEST)


# enroll for a course viewset
class EnrollmentViewSet(ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(
            courses_id=self.kwargs.get("courses_pk")
        ).select_related("courses")

    def create(self, request):
        serializers = EnrollmentSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(student=request.user.student)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentUploadViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete", "patch", "put"]

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = ContentUpload.objects.filter(
            user_id=self.request.user
        ).select_related("user")
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


class ContentManagementViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete", "patch", "put"]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = (
            ContentManagement.objects.filter(is_approved=True)
            .filter(user_id=self.request.user)
            .prefetch_related("content_uploads")
        )
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetContentManagementSerializer
        return ContentManagementSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


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
    queryset = Question.objects.all().order_by("question_bank__course__id")
    permission_classes = [permissions.IsAuthenticated]


class ChoicesViewSet(ModelViewSet):
    serializer_class = ChoicesSerializer
    queryset = Choice.objects.all().order_by("question__id")
    permission_classes = [permissions.IsAuthenticated]


class AssessmentViewSet(ModelViewSet):
    serializer_class = AssessmentSerialier

    def get_queryset(self):
        return 

    def create(self, request):
        serializers = AssessmentSerialier(data= request.data)
        if serializers.is_valid():
            serializers.save(instructor=request.user.instructor)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.error, status=status.HTTP_400_BAD_REQUEST)

class GradeSubmissionView(generics.CreateAPIView):
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        assessment_id = request.data.get('assessment_id')
        answers_data = request.data.get('answers', [])

        try:
            submission = Submission.objects.get(user_id=user_id, assessment_id=assessment_id)
        except Submission.DoesNotExist:
            return Response({"error": "Submission not found"}, status=status.HTTP_404_NOT_FOUND)

        answer_serializer = self.get_serializer(data=answers_data, many=True)
        answer_serializer.is_valid(raise_exception=True)

        answers = []
        for answer_data in answers_data:
            question_id = answer_data['question_id']
            selected_choice_id = answer_data['selected_choice_id']
            text = answer_data.get('text', '')
            try:
                question = Question.objects.get(pk=question_id)
                selected_choice = Choice.objects.get(pk=selected_choice_id)
            except (Question.DoesNotExist, Choice.DoesNotExist):
                return Response({"error": "Invalid question or choice ID"}, status=status.HTTP_400_BAD_REQUEST)

            is_correct = selected_choice.is_correct
            # Here you can implement your logic to calculate points based on correctness
            points = 1.0 if is_correct else 0.0

            answers.append({
                'question': question,
                'text': text,
                'selected_choice': selected_choice,
                'is_correct': is_correct,
                'points': points,
            })

        # Save answers
        Answer.objects.filter(submission=submission).delete()  # Remove previous answers
        Answer.objects.bulk_create([Answer(submission=submission, **answer) for answer in answers])

        # Calculate total score
        total_score = sum(answer['points'] for answer in answers)

        # Update or create grading
        grading, created = Grading.objects.update_or_create(
            student=submission.user,
            assessment=submission.assessment,
            defaults={'score': total_score}
        )

        return Response({"success": "Submission graded successfully", "score": grading.score}, status=status.HTTP_201_CREATED)