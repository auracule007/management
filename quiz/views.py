from rest_framework import permissions, viewsets, response, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from api.models import Instructor, Student
from django.db import transaction
from datetime import datetime, timedelta
from django.utils import timezone
from quiz.models import PointForEachAssignmentSubmission
from performance.models import *
from .models import *
from .serializers import *
from django.db.models import Q
from datetime import datetime, timedelta


class QuestionCategoryViewset(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "put"]
    queryset = QuestionCategory.objects.select_related("instructor").all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = QuestionCategorySerializer


class QuizQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuizQuestionSerializer
    queryset = QuizQuestion.objects.select_related(
        "instructor", "category"
    ).prefetch_related("question")
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.select_related(
        "course", "quiz", "instructor"
    ).prefetch_related("answer_question")
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=7)
        return self.queryset.filter(
            date_created__date__gte=start_of_week,
            date_created__date__lte=end_of_week,
            is_active=True,
        )


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Answer.objects.filter(
            question_id=self.kwargs.get("questions_pk")
        ).select_related("instructor", "student", "question")


class QuizSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = QuizSubmission.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.student:
            student_id = Student.objects.only("id").get(user_id=user.id)
            return (
                self.queryset.filter(student_id=student_id)
                .select_related("student", "instructor")
                .prefetch_related("are_answers")
            )

        if user.instructor:
            instructor_id = Instructor.objects.only("id").get(user_id=user.id)
            return (
                self.queryset.filter(instructor_id=instructor_id)
                .select_related("student", "instructor")
                .prefetch_related("are_answers")
            )
        return self.queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        points_earned = request.data.get("points_earned")
        are_answers_data = request.data.get("are_answers", [])
        request.data.pop("are_answers", None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz_submission = serializer.save()
        are_answers = []
        total_points = 0
        for are_answer_data in are_answers_data:
            are_answer, created = Answer.objects.get_or_create(**are_answer_data)
            are_answers.append(are_answer)
            # calculate each points for right answer
            if are_answer.is_correct:
                total_points += are_answer.points
        quiz_submission.points_earned = total_points
        quiz_submission.save()
        quiz_submission.are_answers.set(are_answers)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ("course__name", "is_ended", "date_created")
    search_fields = ("course__name", "assignment_title", "assignment_description")

    def get_queryset(self):
        assignment = (
            Assignment.objects.filter(
                Q(instructor__user=self.request.user)
                | Q(course__enrollment__student__user=self.request.user)
            )
            .filter(is_ended=False)
            .order_by("date_created")
        )
        return assignment

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instructor_id = request.data.get("instructor_id", None)
        course_id = request.data.get("course_id", None)
        assignment_title = request.data.get("assignment_title", None)
        assignment_description = request.data.get("assignment_description", None)
        assignment_doc = request.data.get("assignment_doc", None)
        date_given = request.data.get("date_given", None)
        date_to_be_submitted = request.data.get("date_to_be_submitted", None)
        is_ended = request.data.get("is_ended", None)

        if assignment_description:
            setattr(instance, "assignment_description", assignment_description)
        if assignment_doc:
            setattr(instance, "assignment_doc", assignment_doc)
        if date_given:
            setattr(instance, "date_given", date_given)
        if date_to_be_submitted:
            setattr(instance, "date_to_be_submitted", date_to_be_submitted)
        if is_ended:
            setattr(instance, "is_ended", is_ended)
        if instructor_id:
            setattr(instance, "instructor_id", instructor_id)
        if course_id:
            setattr(instance, "course_id", course_id)
        if assignment_title:
            setattr(instance, "assignment_title", assignment_title)
        instance.save()
        serializer = AssignmentSerializer(instance)
        return response.Response(serializer.data)


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSubmissionSerializer
    queryset = AssignmentSubmission.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ("is_completed", "date_submitted")
    search_fields = ("submission_context", "assignment__assignment_title")
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UpdateAssignmentSubmissionSerializer
        return self.serializer_class

    def get_queryset(self):
        return (
            self.queryset.filter(user=self.request.user)
            .select_related("assignment", "user")
            .order_by("date_submitted")
        )

    # def perform_create(self, serializer):
    #     print('into the perform create')
    
class AwardForAssignmentSubmissionViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = AwardForAssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = AwardForAssignmentSubmission.objects.select_related(
        "assignment_submission"
    )

    def get_queryset(self):
        return self.queryset.filter(assignment_submission__user=self.request.user)


class AwardForQuizSubmissionViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = AwardForQuizSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = AwardForQuizSubmission.objects.select_related("quiz_submission")

    def get_queryset(self):
        return self.queryset.filter(quiz_submission__user=self.request.user)
