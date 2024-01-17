from django.urls import path, include 
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views 

router = routers.DefaultRouter()
router.register("category", views.CategoryViewSet, basename="category")
router.register("courses", views.CoursesViewSet, basename="courses")
router.register("create_course", views.CreateCoursesViewSet, basename="create_course")
courses_router =routers.NestedDefaultRouter(router, "courses", lookup= "courses")
courses_router.register("enrollment", views.EnrollmentViewSet, basename="courses-enrollment")
router.register("enrollment", views.EnrollmentViewSet, basename="enrollment")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(courses_router.urls))
]