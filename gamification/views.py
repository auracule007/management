from django.shortcuts import render
from rest_framework import permissions, viewsets

from .models import *
from .serializers import *


class PointSystemViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = PointSystemSerializer
    queryset = PointSystem.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).select_related(
            "user", "assignment_submission"
        )


class QuizSubmissionPointSystemViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = QuizSubmissionPointSystemSerializer
    queryset = QuizSubmissionPointSystem.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).select_related(
            "user", "quiz_submission"
        )
