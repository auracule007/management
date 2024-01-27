from rest_framework_nested import routers
from django.urls import path, include 
from .import views

router = routers.DefaultRouter()
router.register('',views.AnalyticsViewSet, basename='analytics')

urlpatterns = [
  path('',include(router.urls) )
]