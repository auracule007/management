from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import SendEmailResetSerializer as BaseSendEmailResetSerializer
from djoser.serializers import (
    PasswordResetConfirmSerializer as BasePasswordResetConfirmSerializer,
)
from .models import *


# users profile
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = "djoserUser"
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "profile_img",
            "user_type",
        )


class SendEmailResetSerializer(BaseSendEmailResetSerializer):
    class Meta(BaseSendEmailResetSerializer):
        fields = ("email",)


class PasswordResetConfirmSerializer(BasePasswordResetConfirmSerializer):
    class Meta(BasePasswordResetConfirmSerializer):
        fields = ("new_password", "re_new_password")


# course category serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class InstructorSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = Instructor
        fields = ["id", "email", "first_name", "last_name"]


# Course serializers
class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    instructor = InstructorSerializer()
    totol_enrolled_student = serializers.SerializerMethodField()

    class Meta:
        model = Courses
        fields = [
            "id",
            "category",
            "instructor",
            "name",
            "description",
            "requirements1",
            "requirements2",
            "requirements3",
            "requirements4",
            "requirements5",
            "price",
            "uploaded",
            "updated",
            "totol_enrolled_student",
        ]

    def get_totol_enrolled_student(self, student: Courses):
        return student.enrollment_set.count()


# Course serializers
class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = [
            "id",
            "category",
            "name",
            "description",
            "requirements1",
            "requirements2",
            "requirements3",
            "requirements4",
            "requirements5",
            "price",
            "uploaded",
            "updated",
        ]


# instructor Serializer
class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ["id", "email", "first_name", "last_name"]


# student Serializer
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "email", "first_name", "last_name"]


# Enrollment Serializer
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["courses", "date_enrolled"]

    def validate_course(self, value):
        if not Enrollment.objects.filter(courses=value).exists():
            return serializers.ValidationError(
                "The Course you are trying to register for is not available"
            )
        return value


# content upload management
class GetContentUploadSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = ContentUpload
        fields = [
            "id",
            "user",
            "content",
            "content_title",
            "content_description",
            "date_uploaded",
            "date_updated",
        ]

    def get_user(self, obj):
        return obj.user.username


class GetContentUploadSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = ContentUpload
        fields = [
            "id",
            "user",
            "content",
            "content_title",
            "content_description",
            "date_uploaded",
            "date_updated",
        ]

    def get_user(self, obj):
        return obj.user.username


class ContentUploadSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ContentUpload
        fields = [
            "id",
            "user_id",
            "content",
            "content_title",
            "content_description",
            "date_uploaded",
            "date_updated",
        ]

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User with the given ID does not exist")


class GetContentManagementSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    content_uploads = serializers.SerializerMethodField()

    class Meta:
        model = ContentManagement
        fields = ["id", "course", "content_uploads", "date_uploaded", "date_updated"]

    def get_content_uploads(self, obj):
        return obj.content_uploads.values(
            "id",
            "user__username",
            "content",
            "content_title",
            "content_description",
            "date_uploaded",
            "date_updated",
        )

    def get_course(self, obj):
        return obj.course.name


class ContentManagementSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField()
    content_uploads = ContentUploadSerializer(many=True, required=False)

    class Meta:
        model = ContentManagement
        fields = ["id", "course_id", "content_uploads", "date_uploaded", "date_updated"]

    def create(self, validated_data):
        course_id = validated_data["course_id"]
        content_uploads = validated_data["content_uploads"]
        content_management = ContentManagement.objects.create(
            course_id=course_id, **validated_data
        )
        for x in content_uploads:
            content_uploads = ContentUpload.objects.filter(**x)
            content_management.content_uploads.set(content_uploads)
        return content_management

    def validate_course_id(self, value):
        if not Courses.object.filter(id=value).exists():
            raise serializers.ValidationError("Course with the given ID does not exist")
        return value

    def save(self, **kwargs):
        course_id = self.validated_data["course_id"]
        content_uploads = self.validated_data["content_uploads"]

        try:
            content_management = ContentManagement.objects.save(course_id=course_id)
            for x in content_uploads:
                content_uploads, _ = ContentUpload.objects.get_or_create(**x)
                content_management.content_uploads.add(content_uploads)

            content_management.save()
            return content_management
        except Exception as e:
            print("Error saving content-management endpoints", e)


# create user
class UserCreateSerializer(BaseUserCreateSerializer):
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "profile_img",
            "user_type",
            "password",
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ChatMessageSerializer(serializers.ModelSerializer):
    receiver_profile = ProfileSerializer(read_only=True)
    sender_profile = ProfileSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = (
            "id",
            "user",
            "sender",
            "receiver",
            "message",
            "is_read",
            "receiver_profile",
            "sender_profile",
            "date_messaged",
        )
