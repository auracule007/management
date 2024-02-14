from django.shortcuts import get_object_or_404
from rest_framework import viewsets,permissions,status
from rest_framework.response import Response
from rest_framework.decorators import action

from register.models import OrderCourse
from register.serializers import CreateOrderCourseSerializer
from subscriptions.emails import send_subscription_confirmation
from utils.flutter import initiate_payment
from .serializers import *
from .models import *
from django.conf import settings


class PlanViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post"]
    serializer_class = PlanSerializer
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]
    def get_queryset(self):
        return Plan.objects.all().filter(is_active=True)
   
    @action(detail=True, methods=['POST'])
    def payment(self, request, pk):
        plan = self.get_object()
        amount = plan.price
        email = request.user.email
        user_id = request.user.id
        first_name = request.user.first_name
        last_name = request.user.last_name
        phone = request.user.phone
        plan_id = plan.pk
        return initiate_payment(amount, email, plan_id,user_id, first_name, last_name, phone)
    
    @action(detail=False, methods=["POST"], url_name='confirm-payment', url_path='confirm-payment')
    def confirm_payment(self, request):
        plan_id = request.GET.get("plan_id")
        if not plan_id:
            return Response({"error": "Missing plan_id parameter"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan = get_object_or_404(Plan, id=plan_id)
        except Plan.DoesNotExist:
            return Response({"error": "Invalid plan_id"}, status=status.HTTP_400_BAD_REQUEST)
        subscribed = Subscription.objects.create(plan_id=plan.id,user_id=self.request.user.id)
        status = request.GET.get("status")
        transaction_id = request.GET.get("transaction_id")
        try:
            if status == 'successful':
                subscribed.pending_status = 'C'
            else: 
                subscribed.pending_status = 'F'
        except Exception as err:
            return Response({'error': err })
        subscribed.transaction_id=transaction_id
        subscribed.save()
        # email notification
        send_subscription_confirmation(plan_id)
        serializer = SubscriptionSerializer(subscribed)
        
        data = {
            "message": "payment was successful",
            "data": serializer.data
        }
        return Response(data)
    
