from rest_framework import serializers
from .models import *

class PlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = Plan
    fields = "__all__"

class SubscriptionSerializer(serializers.ModelSerializer):
  # plan = PlanSerializer(many=True)
  plan_id = serializers.IntegerField()
  user_id = serializers.IntegerField()
  class Meta:
    model = Subscription
    fields = ('id','user_id', 'plan_id' )
