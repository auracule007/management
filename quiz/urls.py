from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register(
    "question-categories", views.QuestionCategoryViewset, basename="question-categories"
)
router.register("quiz-questions", views.QuizQuestionViewSet, basename="quiz-questions")
router.register("questions", views.QuestionViewSet, basename="questions")
router.register(
    "quiz-submissions", views.QuizSubmissionViewSet, basename="quiz-submissions"
)
router.register('assignments', views.AssignmentViewSet, basename='assignments')

# nested routes
answer_router = routers.NestedDefaultRouter(router, "questions", lookup="question")
answer_router.register("answers", views.AnswerViewSet, basename="question-answers")

urlpatterns = [path("", include(router.urls)), path("", include(answer_router.urls))]
