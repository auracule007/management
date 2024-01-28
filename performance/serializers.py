from rest_framework import serializers
from .models import *


class UserPerformanceSerializer(serializers.ModelSerializer):
  user = serializers.StringRelatedField()
  class Meta:
    model = UserPerformance
    fields = ('id','user', 'progress_percentage', 'completion_status')
