from django.shortcuts import render, HttpResponse
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from . serializers import *
from . permissions import * 
from . models import * 


# Create your views here.

# Category viewset
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer 

# Courses viewset 
class CoursesViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    search_fields = ["category__name", "name"]

    def get_queryset(self):
        queryset = Courses.objects.all().order_by("name")
        course_id = self.request.query_params.get('category_id')
        if course_id:
            queryset = Product.objects.filter(category_id=self.request.query_params.get('category_id'))
        return queryset

# create course viewset
class CreateCoursesViewSet(ModelViewSet):
    queryset = Courses.objects.all().order_by("name")
    serializer_class = CreateCourseSerializer
    permission_classes = [IsStudentOrInstructor]

    def create(self, request):
        serializers = CreateCourseSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(instructor=request.user.instructor)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.error, status=status.HTTP_400_BAD_REQUEST)
    
# enroll for a course viewset 
class EnrollmentViewSet(ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializers = EnrollmentSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(student=request.user.student)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)