from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions
from . models import *
from . serializers import *
from utils.paypal import make_paypal_payment, verify_paypal_payment
# Create your views here.

class OrderCourseViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post"]
    serializer_class = OrderCourseSerializer
    permission_classes =[permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.request.user.id  # Assuming you want to filter by the current user
        return OrderCourse.objects.filter(user_id=user_id).prefetch_related("course")

    def get_serializer_class(self):
        if self.request.method =='GET':
            return self.serializer_class
        return CreateOrderCourseSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        ordercourse_id = request.data.get('ordercourse')
        ordercourse = OrderCourse.objects.get(pk=ordercourse_id)

        # Calculate payment amount (for demonstration purposes, let's say it's the total price of the course)
        amount = ordercourse.total()

        # Create a payment with PayPal
        success, payment_id, approval_url = make_paypal_payment(
            amount=amount,
            currency='USD',  # Change to appropriate currency
            return_url=request.build_absolute_uri('/api/payment/success/'),  # URL to redirect after successful payment
            cancel_url=request.build_absolute_uri('/api/payment/cancel/')  # URL to redirect if payment is canceled
        )

        if success:
            # Save the payment details in the database
            Payment.objects.create(
                user=request.user,
                ordercourse=ordercourse,
                amount=amount,
                payment_gateway_transaction_id=payment_id
            )
            # Redirect user to PayPal for payment approval
            return Response({'redirect_url': approval_url}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Failed to create PayPal payment.'}, status=status.HTTP_400_BAD_REQUEST)

class PaymentSuccessView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        payment_id = request.GET.get('paymentId')
        success = verify_paypal_payment(payment_id)
        if success:
            # Payment successful, update payment status in the database
            payment = Payment.objects.get(payment_gateway_transaction_id=payment_id)
            payment.paid = True
            payment.save()
            return Response({'message': 'Payment successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Payment failed.'}, status=status.HTTP_400_BAD_REQUEST)

class PaymentCancelView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Payment canceled.'}, status=status.HTTP_200_OK)


















# class OrderCourseItemViewSet(viewsets.ModelViewSet):
#     http_method_names = ["get"]
#     serializer_class = OrderCourseItemSerializer
    
#     def get_queryset(self):
#         return OrderCourseItem.objects.all()
    
# from utils.paypal import make_paypal_payment, verify_paypal_payment




