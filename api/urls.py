from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register("category", views.CategoryViewSet, basename="category")
router.register("courses", views.CoursesViewSet, basename="courses")
router.register("create_course", views.CreateCoursesViewSet, basename="create_course")
courses_router = routers.NestedDefaultRouter(router, "courses", lookup="courses")
courses_router.register(
    "enrollment", views.EnrollmentViewSet, basename="courses-enrollment"
)
router.register("enrollment", views.EnrollmentViewSet, basename="enrollment")
router.register(
    "content-management", views.ContentManagementViewSet, basename="content-management"
)
router.register("content-upload", views.ContentUploadViewSet, basename="content-upload")
router.register("question-bank", views.QuestionBankViewSet, basename="question-bank")
router.register("question", views.QuestionViewSet, basename="question")

question_router = routers.NestedDefaultRouter(router, "question", lookup="question")
question_router.register(
    "choices", views.ChoicesViewSet, basename="question-choices"
)


urlpatterns = [
    path("", include(router.urls)),
    path("", include(courses_router.urls)),
    path("", include(question_router.urls)),
    path("my-messages/<user_id>", views.ChatMessageView.as_view()),
    path("get-messages/<sender_id>/<receiver_id>/", views.GetAllMessagesView.as_view()),
    path("send-message/", views.SendMessageView.as_view()),
    path("search/<username>", views.SearchUserView.as_view()),
    path('grade-submission/', views.GradeSubmissionView.as_view()),
]
