from django.urls import path, include
from rest_framework_nested import routers
from .import views

router = routers.DefaultRouter()
# router.register('plans', views.PlanViewSet,basename='plans')

urlpatterns = [ 
  # path('',include(router.urls))
]