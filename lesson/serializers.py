from rest_framework import serializers

from api.serializers import GetContentUploadSerializer

from .models import *


class CourseUserProgressSerializer(serializers.ModelSerializer):
    completed_content_upload_lessons = GetContentUploadSerializer(many=True)
    course_progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = CourseUserProgress
        fields = (
            "id",
            "user",
            "course",
            "completed_content_upload_lessons",
            "course_progress_percentage",
        )

    def get_course_progress_percentage(self, obj):
        return obj.course_progress_percentage()
