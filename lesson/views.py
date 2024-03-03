from django.shortcuts import render
from rest_framework import permissions, viewsets

from .serializers import *


class CourseUserProgressViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = CourseUserProgressSerializer
    queryset = CourseUserProgress.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)
