from django.urls import path, include
from .import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('course-progresses', views.CourseUserProgressViewSet, basename='course-progresses')

urlpatterns = [
  path('', include(router.urls))
]