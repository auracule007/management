from django.shortcuts import render, HttpResponse
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
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
            queryset = Courses.objects.filter(category_id=self.request.query_params.get('category_id'))
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
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(courses_id=self.kwargs.get('courses_pk')).select_related('courses')
    
    def create(self, request):
        serializers = EnrollmentSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(student=request.user.student)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
# content management
class ContentManagementViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = ContentManagementSerializer
    queryset = ContentManagement.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        content_uploads_data = request.data.get('content_uploads', [])
        request.data.pop("content_uploads", None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        content_uploads = []
        for tech_category_data in content_uploads_data:
            tech_category, created = ContentUpload.objects.get_or_create(**tech_category_data)
            content_uploads.append(tech_category)

        user.content_uploads.set(content_uploads)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
