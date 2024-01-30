from rest_framework import serializers
from . models import *
from . emails import *


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

class AssignmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Assignment
    fields = "__all__"

  def save(self, *args, **kwargs):
    user = self.validated_data["user"]
    assignment_title = self.validated_data["assignment_title"]
    assignment_description = self.validated_data["assignment_description"]
    assignment_doc = self.validated_data["assignment_doc"]
    date_given = self.validated_data["date_given"]
    date_to_be_submitted = self.validated_data["date_to_be_submitted"]
    # date_created = self.validated_data["date_created"]
    is_completed = self.validated_data["is_completed"]

    assignment = Assignment.objects.create(
      user = user,
      assignment_title = assignment_title,
      assignment_description = assignment_description,
      assignment_doc = assignment_doc,
      date_given = date_given,
      date_to_be_submitted = date_to_be_submitted,
      # date_created = date_created,
      is_completed = is_completed,
    )
    assignment_due_date_email(user, assignment_title, date_given, date_to_be_submitted)
    return assignment