from django.urls import path, include
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("forums", forum_views.ForumQuestionViewSet, basename="forum_question")

# nested router
forum_router = routers.NestedDefaultRouter(router, "forums", lookup="forum_question")
forum_router.register(
    "answers", forum_views.ForumAnswerViewSet, basename="forum_question-answers"
)


urlpatterns = [
  path('', include(router.urls)),
  path("", include(forum_router.urls)),
]