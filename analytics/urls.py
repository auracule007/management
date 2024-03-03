from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register("", views.AnalyticsViewSet, basename="analytics")
router.register('dashboard', views.UserDashboard, basename='dashboard')


urlpatterns = [path("", include(router.urls))]
