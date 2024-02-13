from rest_framework import viewsets,permissions,status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import *
from .models import *
from django.conf import settings

# class SubscriptionViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Subscription.objects.all()
#     def create(self, request, pk=None):
#         plan = Plan.objects.get(pk=pk)
#         serializer = SubscriptionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         stripe.api_key = settings.STRIPE_SECRET_KEY

#         try:
#             subscription = stripe.Subscription.create(
#                 customer=request.user.stripe_customer_id,
#                 items=[{"price": plan.stripe_price_id}],
#             )

#             user = self.request.user
#             user.stripe_customer_id = subscription.customer
#             user.save()

#             created_subscription = Subscription.objects.create(
#                 user=request.user,
#                 plan=plan,
#                 stripe_subscription_id=subscription.id,
#             )

#             serialized_data = SubscriptionSerializer(created_subscription).data
#             return Response(serialized_data, status=status.HTTP_201_CREATED)

#         except error.StripeError as e:
#             return Response({"error": e.api_message}, status=status.HTTP_400_BAD_REQUEST)

class PlanViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post"]
    serializer_class = PlanSerializer
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]
    def get_queryset(self):
        return Plan.objects.all().filter(is_active=True)

    @action(detail=True, methods=['POST'], serializer_class=SubscriptionSerializer)
    def payment(self, request, pk):
        plan = self.get_object()
        user = request.user.username
        price = plan.price
        return Response({'price': price, 'user': user})

    
    # @action(detail=False, methods=["POST"], url_name='confirm-payment', url_path='confirm-payment')
    # def confirm_payment(self, request):
    #     order_id = request.GET.get("order_id")
    #     order =get_object_or_404(OrderCourse, id=order_id) 
    #     order.pending_status = "C"
    #     order.save()
    #     serializer = CreateOrderCourseSerializer(order)
        
    #     data = {
    #         "message": "payment was successful",
    #         "data": serializer.data
    #     }
    #     return Response(data)
    
