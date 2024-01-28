from rest_framework import viewsets, permissions
from.serializers import *
from .models import UserPerformance


class UserPerformanceViewSet(viewsets.ModelViewSet):
  http_method_names = ['get']
  serializer_class = UserPerformanceSerializer
  queryset = UserPerformance.objects.select_related('user')
  permission_classes = [permissions.IsAuthenticated]

