from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import *




class CourseUserProgressViewSet(viewsets.ModelViewSet):
  serializer_class = CourseUserProgressSerializer
  queryset = CourseUserProgress.objects.all()
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    return self.queryset.filter(user_id=self.request.user.id)