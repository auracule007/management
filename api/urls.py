from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register("category", views.CategoryViewSet, basename="category")
# router.register("courses", views.CoursesViewSet, basename="courses")
router.register("contact", views.ContactViewSet, basename="contact")
router.register("create_course", views.CreateCoursesViewSet, basename="create_course")
router.register("enrollment", views.EnrollmentViewSet, basename="enrollment")
router.register('modules', views.ModuleViewSet, basename="modules")

certificate_router = routers.NestedDefaultRouter(router, "enrollment", lookup="enrollment")
certificate_router.register('certificate', views.CertificateViewSet, basename="certificate")
cat_router = routers.NestedDefaultRouter(router, "category", lookup="category")
cat_router.register("courses", views.CoursesViewSet, basename="category-courses")
# content_router = routers.NestedDefaultRouter(cat_router,"courses", lookup="courses")
# content_router.register('content-uploads', views.ContentUploadViewSet, basename="courses-uploads")
course_requirement = routers.NestedDefaultRouter(cat_router, "courses",lookup="courses")
course_requirement.register('requirements',views.CourseRequirementViewSet, basename="courses-requirements")
course_module = routers.NestedDefaultRouter(cat_router, "courses",lookup="courses")
course_module.register('module',views.ModuleViewSet, basename="courses-module")

# router.register(
#     "content-managements",
#     views.ContentManagementViewSet,
#     basename="content-managements",
# )

# router.register("question-bank", views.QuestionBankViewSet, basename="question-bank")
# router.register("question", views.QuestionViewSet, basename="question")
# router.register(
#     "content-managements",
#     views.ContentManagementViewSet,
#     basename="content-managements",
# )
# router.register(
#     "content-uploads", views.ContentUploadViewSet, basename="content-uploads"
# )
# router.register("question-bank", views.QuestionBankViewSet, basename="question-bank")
# router.register("question", views.QuestionViewSet, basename="question")
router.register("admin", views.AdminDashboardViewSet, basename="admin")
router.register("user-lists", views.UserViewSet, basename="user-lists")
router.register("course-events", views.CourseEventViewset, basename="course-events")
router.register("course-ratings", views.CourseRatingViewSet, basename="course-ratings")

# nested routes
# question_router = routers.NestedDefaultRouter(router, "question", lookup="question")
# question_router.register("choices", views.ChoicesViewSet, basename="question-choices")



# nested route
# courses_router = routers.NestedDefaultRouter(router, "courses", lookup="courses")
# courses_router.register(
#     "enrollment", views.EnrollmentViewSet, basename="courses-enrollment"
# )
# content_router = routers.NestedDefaultRouter(router,"courses", lookup="courses")
# content_router.register('content-uploads', views.ContentUploadViewSet, basename="courses-content-uploads")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(cat_router.urls)),
    path("", include(course_requirement.urls)),
    path('', include(certificate_router.urls)),
    path('', include(course_module.urls)),
    path("my-messages/<user_id>", views.ChatMessageView.as_view()),
    path("get-messages/<sender_id>/<receiver_id>/", views.GetAllMessagesView.as_view()),
    path("send-message/", views.SendMessageView.as_view()),
    # path('auth/users/', views.UserCreateView.as_view(), name='user-create'),
    path("search/<username>", views.SearchUserView.as_view()),
    path("grade-submission/", views.GradeSubmissionView.as_view()),
]
