from django.shortcuts import render
from rest_framework import viewsets, permissions
from . models import *
from . serializers import *

# Create your views here.

# class CartCoursesViewSet(viewsets.ModelViewSet):
#     http_method_names = ["get", "post"]
#     queryset = CartCourses.objects.all().prefetch_related("cartcoursesitem_set__course")
#     serializer_class = CartCoursesSerializer

# class CartCoursesItemViewSet(viewsets.ModelViewSet):
#     http_method_names = ["get", "post","patch", "delete"]
#     serializer_class = CartCoursesItemSerializers
    
#     def get_queryset(self):
#         return CartCoursesItem.objects.select_related("course").filter(course_id=self.kwargs["cartcourses_pk"])
    
# class OrderCourseViewSet(viewsets.ModelViewSet):
    