from django.db.models import Avg, Count, Max, Min, Sum
from rest_framework import permissions, response, viewsets
from rest_framework.decorators import action

from api.models import *
from api.serializers import CourseSerializer

from .serializers import *
from quiz.models import Question


class AnalyticsViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    queryset = Courses.objects.select_related(
        "category", "instructor"
    ).prefetch_related("courserating_set", "coursereview_set")

    def get_serializer_class(self):
        if self.action == "ratings":
            return CourseRatingSerializer
        elif self.action == "student_completed_course":
            return StudentCompletedCourseSerializer
        return CourseAnalyticSerializer

    @action(detail=False, methods=["get"])
    def ratings(self, request, *args, **kwargs):
        course_ratings = Courses.objects.annotate(
            max_rating=Max("courserating__value"),
            min_rating=Min("courserating__value"),
            avg_rating=Avg("courserating__value"),
        ).distinct()

        serializer = CourseRatingSerializer(course_ratings, many=True)
        return response.Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_name="student-completed-courses",
        url_path="student-completed-courses",
    )
    def student_completed_course(self, request, *args, **kwargs):
        course_completed = (
            Courses.objects.filter(enrollment__completion_status=True)
            .select_related("category")
            .annotate(number_of_students=Count("enrollment__student"))
            .distinct()
        )
        serializer = StudentCompletedCourseSerializer(course_completed, many=True)
        return response.Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_name="most-viewed-course",
        url_path="most-viewed-course",
    )
    def most_viewed_course(self, request, *args, **kwargs):
        courses = Courses.objects.all().select_related("category", "instructor")
        serializer = CourseSerializer(courses, many=True)
        return response.Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_name="most-purchased-course",
        url_path="most-purchased-course",
    )
    def most_purchased_course(self, request, *args, **kwargs):
        return response.Response("Most purchased course")


class UserDashboard(viewsets.ModelViewSet):
    http_method_names = ["get"]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CountDetailSerializer
    queryset = Enrollment.objects.select_related("student", "courses")

    @action(detail=False, methods=["get"], url_name='dashboard-data', url_path='dashboard-data')
    def dashboard_data(self, request, *args, **kwargs):
        completed_courses = (
            self.queryset.filter(student__user=self.request.user)
            .filter(completion_status=True)
            .aggregate(total_completed=Count("id"))
        )

        to_do_courses = (
            self.queryset.filter(student__user=self.request.user)
            .filter(completion_status=False)
            .aggregate(total_to_do=Count("id"))
        )

        task_completed = (
            Question.objects.filter(course__enrollment__student__user=self.request.user)
            .filter(is_completed=True, is_active=True)
            .aggregate(total_tasks_completed=Count("id"))
        )

        certificate_count = Certificate.get_certificate_count(self.request.user)
        all_certificates = Certificate.objects.filter(enrollment__student__user=self.request.user).values().all()

        data = {
            "completed_courses": completed_courses["total_completed"],
            "to_do_courses": to_do_courses["total_to_do"],
            "tasks_completed": task_completed["total_tasks_completed"],
            "certificate_count": certificate_count,
            "all_certificates": all_certificates,
        }

        return response.Response(data)


# class UserDashboard(viewsets.ModelViewSet):
#     http_method_names = ["get"]
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = CountDetailSerializer
#     queryset = Enrollment.objects.select_related("student", "courses")

#     @action(detail=False, methods=["get"], url_name='completed-courses', url_path='completed-courses')
#     def completed_courses(self, request, *args, **kwargs):
#         enrolled_courses = (
#             self.queryset.filter(student__user=self.request.user).filter(completion_status=True).aggregate(total_number=Count("id"))
#             )
#         serializer = CountDetailSerializer(enrolled_courses)
#         return response.Response(serializer.data)

#     @action(detail=False, methods=["get"], url_name='to-do-courses', url_path='to-do-courses')
#     def to_do_courses(self, request, *args, **kwargs):
#         enrolled_courses = (
#             self.queryset.filter(student__user=self.request.user).filter(completion_status=False).aggregate(total_number=Count("id"))
#             )
#         serializer = CountDetailSerializer(enrolled_courses)
#         return response.Response(serializer.data)

#     @action(detail=False, methods=["get"], url_name='task-completed', url_path='task-completed')
#     def task_completed(self, request, *args, **kwargs):
#         questions = Question.objects.filter(course__enrollment__student__user=self.request.user).filter(is_completed=True, is_active=True).aggregate(total_number=Count("id"))
#         serializer = CountDetailSerializer(questions)
#         return response.Response(serializer.data)
    
    