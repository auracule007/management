from django.db.models import Sum
from rest_framework import serializers

from quiz.models import AssignmentSubmission
from quiz.serializers import AssignmentSubmissionSerializer

from .models import *


class PointSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointSystem
        fields = (
            "id",
            "user",
            "points_earned",
            "assignment_submission",
            "date_updated",
            "date_created",
        )


class QuizSubmissionPointSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSubmissionPointSystem
        fields = (
            "id",
            "user",
            "points_earned",
            "quiz_submission",
            "date_updated",
            "date_created",
        )
