from rest_framework import serializers
from .models import *


class QuestionCategorySerializer(serializers.ModelSerializer):
  instructor_id = serializers.IntegerField()
  class Meta:
    model = QuestionCategory
    fields = ('id','instructor_id', 'name')

  def validate_instructor_id(self, value):
    if not Instructor.objects.filter(id=value).exists():
      raise serializers.ValidationError('the given intructor id is not valid' )
    return value


class QuizQuestionSerializer(serializers.ModelSerializer):
  class Meta:
    model = QuizQuestion
    fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
  class Meta:
    ref_name = 'Question quiz'
    model = Question
    fields = ['id','instructor', 'course', 'quiz', 'technique', 'difficulty','date_created', 'date_updated', 'is_active']

class AnswerSerializer(serializers.ModelSerializer):
  class Meta:
    ref_name = 'Answer question'
    model = Answer
    fields = '__all__'