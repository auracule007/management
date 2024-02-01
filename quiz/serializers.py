from rest_framework import serializers

from api.models import Instructor, Student
from .models import *
from utils.validators import validate_id

class QuestionCategorySerializer(serializers.ModelSerializer):
    instructor_id = serializers.IntegerField()

    class Meta:
        model = QuestionCategory
        fields = ("id", "instructor_id", "name")

    def validate_instructor_id(self, value):
        if not Instructor.objects.filter(id=value).exists():
            raise serializers.ValidationError("the given intructor id is not valid")
        return value


class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "Question quiz"
        model = Question
        fields = [
            "id",
            "instructor",
            "course",
            "quiz",
            "technique",
            "difficulty",
            "date_created",
            "date_updated",
            "is_active",
        ]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "Answer question"
        model = Answer
        fields = "__all__"


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = (
            "id",
            "user",
            "assignment",
            "assignment_submission_doc",
            "date_submitted",
        )

class AnswerTheQuestionSerializer(serializers.ModelSerializer):
    instructor_id = serializers.IntegerField()
    student_id = serializers.IntegerField()
    question_id = serializers.IntegerField()
    class Meta:
        ref_name = 'Answer_the_question'
        model = Answer
        fields = ('id','instructor_id','student_id','question_id','answer_text')

    def validate_question_id(self, value):
        return validate_id(
            Question, value
        )
    def validate_student_id(self, value):
        return validate_id(
            Student, value
        )
    def validate_instructor_id(self, value):
        return validate_id(
            Instructor, value
        )

class QuizSubmissionSerializer(serializers.ModelSerializer):
    are_answers = AnswerTheQuestionSerializer(many=True, required=False)
    instructor_id = serializers.IntegerField()
    student_id = serializers.IntegerField()
    question_id = serializers.IntegerField()
    class Meta:
        model = QuizSubmission
        fields = (
            "id",
            "instructor_id",
            "student_id",
            "question_id",
            "are_answers",
            "points_earned",
            "submitted_date",
        )    
        read_only_fields = ('points_earned',)

    def validate_question_id(self, value):
        return validate_id(
            Question, value
        )
    def validate_student_id(self, value):
        return validate_id(
            Student, value
        )
    def validate_instructor_id(self, value):
        return validate_id(
            Instructor, value
        )

 
