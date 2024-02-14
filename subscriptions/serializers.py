from rest_framework import serializers

from utils.validators import validate_id
from .models import *

class PlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = Plan
    fields = "__all__"

class SubscriptionSerializer(serializers.ModelSerializer):
  plan_id = serializers.IntegerField()
  user_id = serializers.IntegerField()
  class Meta:
    model = Subscription
    fields = ('id','user_id', 'plan_id' )
  def validate_user_id(self, value):
    return (User, value)
  def validate_plan_id(self, value):
    return validate_id(Plan, value)
  
  def create(self, validated_data):
    user_id = self.context.get('user_id')
    plan_id = validated_data['plan_id']
    return Subscription.objects.create(user_id=user_id, plan_id=plan_id, **validated_data)
  