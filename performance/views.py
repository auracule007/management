from rest_framework import permissions, viewsets

from .models import UserPerformance
from .serializers import *


class UserPerformanceViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = UserPerformanceSerializer
    queryset = UserPerformance.objects.select_related("user")
    permission_classes = [permissions.IsAuthenticated]

class UserQuizPerformanceViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = UserQuizPerformanceSerializer
    queryset = UserQuizPerformance.objects.select_related("user")
    permission_classes = [permissions.IsAuthenticated]
