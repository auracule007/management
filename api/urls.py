from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from forum import views as forum_views

from . import views

router = routers.DefaultRouter()
router.register("category", views.CategoryViewSet, basename="category")
router.register("courses", views.CoursesViewSet, basename="courses")
router.register("create_course", views.CreateCoursesViewSet, basename="create_course")
router.register("enrollment", views.EnrollmentViewSet, basename="enrollment")
router.register(
    "content-management", views.ContentManagementViewSet, basename="content-management"
)
router.register("content-upload", views.ContentUploadViewSet, basename="content-upload")
<<<<<<< HEAD
router.register("question-bank", views.QuestionBankViewSet, basename="question-bank")
router.register("question", views.QuestionViewSet, basename="question")

question_router = routers.NestedDefaultRouter(router, "question", lookup="question")
question_router.register(
    "choices", views.ChoicesViewSet, basename="question-choices"
=======
router.register("forums", forum_views.ForumQuestionViewSet, basename="forum_question")

# nested route
courses_router = routers.NestedDefaultRouter(router, "courses", lookup="courses")
courses_router.register(
    "enrollment", views.EnrollmentViewSet, basename="courses-enrollment"
)

forum_router = routers.NestedDefaultRouter(router, "forums", lookup="forum_question")
forum_router.register(
    "answers", forum_views.ForumAnswerViewSet, basename="forum_question-answers"
>>>>>>> 42f7c94 (forum endpoints and upvotes)
)


urlpatterns = [
    path("", include(router.urls)),
    path("", include(courses_router.urls)),
<<<<<<< HEAD
    path("", include(question_router.urls)),
=======
    path("", include(forum_router.urls)),
>>>>>>> 42f7c94 (forum endpoints and upvotes)
    path("my-messages/<user_id>", views.ChatMessageView.as_view()),
    path("get-messages/<sender_id>/<receiver_id>/", views.GetAllMessagesView.as_view()),
    path("send-message/", views.SendMessageView.as_view()),
    path("search/<username>", views.SearchUserView.as_view()),
    path('grade-submission/', views.GradeSubmissionView.as_view()),
]
