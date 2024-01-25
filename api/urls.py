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
    "content-managements", views.ContentManagementViewSet, basename="content-managements"
)
router.register("content-uploads", views.ContentUploadViewSet, basename="content-uploads")
router.register("question-bank", views.QuestionBankViewSet, basename="question-bank")
router.register("question", views.QuestionViewSet, basename="question")
router.register('admin',views.AdminDashboardViewSet, basename="admin")
router.register('user-lists', views.UserViewSet,basename='user-lists')
router.register("forums", forum_views.ForumQuestionViewSet, basename="forum_question")

# nested routes
question_router = routers.NestedDefaultRouter(router, "question", lookup="question")
question_router.register(
    "choices", views.ChoicesViewSet, basename="question-choices")


# nested route
courses_router = routers.NestedDefaultRouter(router, "courses", lookup="courses")
courses_router.register(
    "enrollment", views.EnrollmentViewSet, basename="courses-enrollment"
)

forum_router = routers.NestedDefaultRouter(router, "forums", lookup="forum_question")
forum_router.register(
    "answers", forum_views.ForumAnswerViewSet, basename="forum_question-answers"
)


urlpatterns = [
    path("", include(router.urls)),
    path("", include(courses_router.urls)),
    path("", include(question_router.urls)),
    path("", include(forum_router.urls)),
    path("my-messages/<user_id>", views.ChatMessageView.as_view()),
    path("get-messages/<sender_id>/<receiver_id>/", views.GetAllMessagesView.as_view()),
    path("send-message/", views.SendMessageView.as_view()),
    path("search/<username>", views.SearchUserView.as_view()),
    path('grade-submission/', views.GradeSubmissionView.as_view()),
]
