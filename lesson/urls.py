from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register(
    "course-progresses", views.CourseUserProgressViewSet, basename="course-progresses"
)

urlpatterns = [path("", include(router.urls))]
