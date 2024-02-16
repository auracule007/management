from django.urls import path, include
from rest_framework_nested import routers
from .import views
# router = routers.DefaultRouter()

urlpatterns = [
  # path('', include(router.urls))
  path('', views.index)
]