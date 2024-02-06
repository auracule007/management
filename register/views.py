from django.shortcuts import render
from rest_framework import viewsets, permissions
from . models import *
from . serializers import *

# Create your views here.

class OrderCourseViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = OrderCourse.objects.all().prefetch_related("ordercourseitem_set__course")
    serializer_class = OrderCourseSerializer
    permission_classes =[permissions.IsAuthenticatedOrReadOnly]
    def get_serializer_class(self):
        if self.request.method =='GET':
            return self.serializer_class
        return CreateOrderCourseSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# class OrderCourseItemViewSet(viewsets.ModelViewSet):
#     http_method_names = ["get"]
#     serializer_class = OrderCourseItemSerializer
    
#     def get_queryset(self):
#         return OrderCourseItem.objects.all()
    
# from utils.paypal import make_paypal_payment, verify_paypal_payment

































































































































































# class CartCoursesItemViewSet(viewsets.ModelViewSet):
#     http_method_names = ["get", "post","patch", "delete"]
#     serializer_class = CartCoursesItemSerializers
    
#     def get_queryset(self):
#         return CartCoursesItem.objects.select_related("course").filter(course_id=self.kwargs["cartcourses_pk"])
    
# class OrderCourseViewSet(viewsets.ModelViewSet):
    
    # queryset = OrderCourse.objects.all().prefetch_related("ordercoursesitem_set__course")