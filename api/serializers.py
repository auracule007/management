from rest_framework import serializers
from rest_framework.serializers import Serializer
from djoser.serializers import UserCreateSerializer as  BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import SendEmailResetSerializer as BaseSendEmailResetSerializer
from djoser.serializers import PasswordResetConfirmSerializer as BasePasswordResetConfirmSerializer
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import ValidationError
from . models import * 



# users profile
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name= 'djoserUser'
        fields=('id','username','first_name','last_name','email', 'phone', 'profile_img','user_type')

class SendEmailResetSerializer(BaseSendEmailResetSerializer):
    class Meta(BaseSendEmailResetSerializer):
        fields = ('email',) 

class PasswordResetConfirmSerializer(BasePasswordResetConfirmSerializer):
    class Meta(BasePasswordResetConfirmSerializer):
        fields = ('new_password', 're_new_password')

# course category serializer 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","name", "description"]


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
        fields = ["id","category", "instructor","name", "description", "requirements1",
         "requirements2", "requirements3", "requirements4", "requirements5", "price", "uploaded", "updated", "totol_enrolled_student"]

    def get_totol_enrolled_student(self, student: Courses):
        return student.enrollment_set.count()

# Course serializers
class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Courses 
        fields = ["id", "category" ,"name", "description", "requirements1",
         "requirements2", "requirements3", "requirements4", "requirements5", "price", "uploaded", "updated"]


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
            return serializers.ValidationError("The Course you are trying to register for is not available")
        return value 

# content upload
class ContentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentUpload
        fields = ['id','user_id','content','content_title','content_description','date_uploaded','date_updated']

# content management
class ContentManagementSerializer(serializers.ModelSerializer):
    content_uploads = ContentUploadSerializer(many=True, required=False)
    class Meta:
        model = ContentManagement
        fields = ['id','course_id','content_uploads','date_uploaded','date_updated']

# create user 
class UserCreateSerializer(BaseUserCreateSerializer):
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES)
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('username','first_name','last_name','email', 'phone', 'profile_img','user_type', 'password')

# question bank serializer for all course module
class QuestionBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBank
        fields = []