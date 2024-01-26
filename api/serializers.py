from djoser.serializers import \
    PasswordResetConfirmSerializer as BasePasswordResetConfirmSerializer
from djoser.serializers import \
    SendEmailResetSerializer as BaseSendEmailResetSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from django.core.mail import send_mail
from django.template.loader import render_to_string
from  . emails import *
from .models import *


# users profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'User Profile'
        model = Profile
        fields = "__all__"
        ref_name = 'Profile'

class UserSerializer(BaseUserSerializer): 
    profile = ProfileSerializer()
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'Profile User'
        fields = BaseUserSerializer.Meta.fields + ("profile",)


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
    total_enrolled_student = serializers.SerializerMethodField()

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
            "total_enrolled_student",
        ]

    def get_total_enrolled_student(self, student: Courses):
        return student.enrollment_set.count()
from django.core.exceptions import ObjectDoesNotExist


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

    def validate_courses(self, value):
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
    user = serializers.CharField(source="user.username", read_only=True)

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

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User with the given ID does not exist")


class GetContentManagementSerializer(serializers.ModelSerializer):
    # course = serializers.SerializerMethodField()
    content_uploads = serializers.SerializerMethodField()
    user = serializers.CharField(source="user.username")

    class Meta:
        model = ContentManagement
        fields = [
            "id",
            "user",
            "course_id",
            "content_uploads",
            "date_uploaded",
            "date_updated",
        ]

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

    # def get_course(self, obj):
    #     return obj.course.name


class ContentManagementSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField()
    content_uploads = ContentUploadSerializer(many=True, required=False)

    class Meta:
        model = ContentManagement
        fields = ["id", "course_id", "content_uploads", "date_uploaded", "date_updated"]

    def validate_course_id(self, value):
        if not Courses.objects.filter(id=value).exists():
            raise serializers.ValidationError("Course with the given ID does not exist")
        return value

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


# question bank serializer for all course module
class QuestionBankSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=True)
    class Meta:
        model = QuestionBank
        fields = ["instructor", "course", "name", "description"]

    def validate_course__id(self, value):
        if not QuestionBank.objects.filter(course__id=value).exists():
            return serializers.ValidationError("The course ID you are trying to get isn't available")
        raise value 

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["question_bank", "student", "text", "question_type", "created_at", "updated_at"]

    
class ChoicesSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True, required=True)
    class Meta:
        model = Choice
        fields = ["question", "text", "is_correct"] 

class AssessmentSerialier(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ["course", "questions", "title", "descrpition", "time_limit", "created_at", "updated_at"]

class SubmissionSerializer(serializers.ModelSerializer):
    assessment = AssessmentSerialier(many=True, required=True)
    course = CourseSerializer()

    class Meta:
        model = Submission
        fields = ["assessment", "user", "submitted_at"]

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["submission", "student", "question", "text", "selected_choice", "is_correct", "points"]

class GradingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grading
        fields = ["assessment", "student", "score", "feedback"]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        ref_name = 'Profile'


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
            "sender_profile",
            "receiver",
            "receiver_profile",
            "message",
            "is_read",
            "date_messaged",
        )


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','username','email','is_staff')

class CourseEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEvent
        fields = "__all__"