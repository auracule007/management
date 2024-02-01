from rest_framework import permissions, viewsets, response, status

from api.models import Instructor, Student
from django.db import transaction
from .models import *
from .serializers import *


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
    queryset = (
        Question.objects.select_related("course", "quiz", "instructor")
        .prefetch_related("answer_question")
        .filter(is_active=True)
    )
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Answer.objects.filter(
            question_id=self.kwargs.get("question_pk")
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
            instructor_id = Instructor.objects.only("id").get(
                user_id=user.id
            )
            return (
                self.queryset.filter(instructor_id=instructor_id)
                .select_related("student", "instructor")
                .prefetch_related("are_answers")
            )
        return self.queryset
    @transaction.atomic
    def create(self, request,*args, **kwargs):
        points_earned = request.data.get('points_earned')
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
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class AssignmentViewSet(viewsets.ModelViewSet):
  queryset = Assignment.objects.all()
#   serializer_class = AssignmentSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]


  
 