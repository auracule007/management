from django.db.models import Avg, Count, Max, Min
from rest_framework import permissions, response, viewsets
from rest_framework.decorators import action

from api.models import *
from api.serializers import CourseSerializer

from .serializers import *


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
        return response.Response("Most viewed course")

    @action(
        detail=False,
        methods=["get"],
        url_name="most-purchased-course",
        url_path="most-purchased-course",
    )
    def most_purchased_course(self, request, *args, **kwargs):
        return response.Response("Most purchased course")
