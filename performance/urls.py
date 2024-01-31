from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register(
    "user-performances", views.UserPerformanceViewSet, basename="user-performances"
)

urlpatterns = [path("", include(router.urls))]
