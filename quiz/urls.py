from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register(
    "question-categories", views.QuestionCategoryViewset, basename="question-categories"
)
question_router = routers.NestedDefaultRouter(router, "question-categories", lookup="question_categories")
question_router.register("questions", views.QuestionViewSet, basename="question_categories-questions")
answer_router = routers.NestedDefaultRouter(question_router, "questions", lookup="questions")
answer_router.register("answers", views.AnswerViewSet, basename="questions-answers")


router.register("quiz-questions", views.QuizQuestionViewSet, basename="quiz-questions")
# router.register("questions", views.QuestionViewSet, basename="questions")
router.register(
    "quiz-submissions", views.QuizSubmissionViewSet, basename="quiz-submissions"
)
router.register('assignments', views.AssignmentViewSet, basename='assignments')
router.register('assignment-submissions', views.AssignmentSubmissionViewSet, basename='assignment-submissions')

# nested routes
# answer_router = routers.NestedDefaultRouter(router, "questions", lookup="question")
# answer_router.register("answers", views.AnswerViewSet, basename="question-answers")

urlpatterns = [
    path("", include(router.urls)), 
    path("", include(question_router.urls)),
    path("", include(answer_router.urls))
]
