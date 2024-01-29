from .serializers import *
from rest_framework import viewsets, permissions
from .models import *


class QuestionCategoryViewset(viewsets.ModelViewSet):
  http_method_names = ['get', 'post', 'patch', 'delete', 'put']
  queryset = QuestionCategory.objects.select_related('instructor').all()
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  serializer_class = QuestionCategorySerializer


class QuizQuestionViewSet(viewsets.ModelViewSet):
  serializer_class = QuizQuestionSerializer
  queryset = QuizQuestion.objects.select_related('instructor', 'category').prefetch_related('question')
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class QuestionViewSet(viewsets.ModelViewSet):
  serializer_class = QuestionSerializer
  queryset = Question.objects.select_related('course','quiz','instructor').prefetch_related('answer_question').filter(is_active=True)
  permission_classes =[permissions.IsAuthenticatedOrReadOnly]


class AnswerViewSet(viewsets.ModelViewSet):
  serializer_class= AnswerSerializer
  permission_classes =[permissions.IsAuthenticatedOrReadOnly]

  def get_queryset(self):
    return Answer.objects.filter(question_id=self.kwargs.get('question_pk')).select_related('instructor','student','question')
  
class AssignmentViewSet(viewsets.ModelViewSet):
  serializer_class = AssignmentSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]

  def get_queryset(self):
    return Assignment.objects.filter()