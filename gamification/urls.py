from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

router.register(
    "assignment-points", views.PointSystemViewSet, basename="assignment-points"
)
router.register(
    "quiz-points", views.QuizSubmissionPointSystemViewSet, basename="quiz-points"
)
urlpatterns = [path("", include(router.urls))]
