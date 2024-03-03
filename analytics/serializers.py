from django.db.models import Avg, Max, Min
from rest_framework import serializers

from api.models import *


class CountDetailSerializer(serializers.Serializer):
    # courses= serializers.CharField(max_length=255)
    # total_number = serializers.IntegerField()
    total_number = serializers.IntegerField()


class CourseAnalyticSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        ref_name = "CourseAnalytics"
        model = Courses
        fields = ("id", "category", "name")


class CourseRatingSerializer(serializers.ModelSerializer):
    min_rating = serializers.IntegerField()
    max_rating = serializers.IntegerField()
    avg_rating = serializers.IntegerField()

    class Meta:
        ref_name = "Course Rating"
        model = Courses
        fields = ("id", "name", "min_rating", "max_rating", "avg_rating")


class StudentCompletedCourseSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    number_of_students = serializers.IntegerField()

    class Meta:
        ref_name = "StudentCompletedCourse"
        model = Courses
        fields = ("id", "category", "name", "number_of_students")

    def get_number_of_students(self, obj):
        return (
            Enrollment.objects.filter(course_id=obj.id)
            .filter(completion_status=True)
            .count()
            .distinct(True)
        )
