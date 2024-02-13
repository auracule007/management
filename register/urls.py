from django.urls import path, include 
from rest_framework_nested import routers 
from rest_framework_nested.routers import DefaultRouter
from . import views


router = routers.DefaultRouter()

# router.register("ordercourse", views.OrderCourseViewSet, basename="ordercourse")


urlpatterns = [
    # path("",include(router.urls)),
    # path('payment/create/', views.PaymentCreateView.as_view(), name='payment-create'),
    # path('payment/success/', views.PaymentSuccessView.as_view(), name='payment-success'),
    # path('payment/cancel/', views.PaymentCancelView.as_view(), name='payment-cancel'),
]