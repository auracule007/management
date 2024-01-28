from django.urls import path, include
from .import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('user-performances', views.UserPerformanceViewSet, basename='user-performances')

urlpatterns = [
  path('',include(router.urls))
]