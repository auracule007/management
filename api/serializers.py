from django.db.models import Sum
from djoser.serializers import (
    PasswordResetConfirmSerializer as BasePasswordResetConfirmSerializer,
)
from djoser.serializers import SendEmailResetSerializer as BaseSendEmailResetSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from api.emails import update_course_email, send_content_upload_mail
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from gamification.models import PointSystem, QuizSubmissionPointSystem
from utils.validators import validate_id
from .emails import *
from .models import *
from quiz.serializers import QuestionSerializer


class BaseTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token


class UserTokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data["id"] = self.user.id
        data["username"] = self.user.username
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        data["email"] = self.user.email
        data["user_type"] = self.user.user_type
        data["is_active"] = self.user.is_active
        data["is_superuser"] = self.user.is_superuser
        data["is_staff"] = self.user.is_staff
        try:
            if self.user.user_type == "Student":
                data["student_id"] = self.user.student.id
            elif self.user.user_type == "Instructor":
                data["instructor_id"] = self.user.instructor.id
            else:
                data["type"] = "No user type"

        except Exception as err:
            raise serializers.ValidationError(err)
        return data


# users profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "User Profile"
        model = Profile
        fields = "__all__"
        ref_name = "Profile"


class UserSerializer(BaseUserSerializer):
    profile = ProfileSerializer()
    total_points_earned_for_assignments = serializers.SerializerMethodField()
    total_points_earned_for_quizzes = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        ref_name = "Profile User"
        fields = (
            "id",
            "user_type",
            "first_name",
            "last_name",
            "email",
            "profile_img",
            "phone",
        ) + (
            "profile",
            "total_points_earned_for_assignments",
            "total_points_earned_for_quizzes",
        )
        # fields = BaseUserSerializer.Meta.fields + ("profile", "total_points_earned_for_assignments", "total_points_earned_for_quizzes")

    def get_total_points_earned_for_quizzes(self, obj):
        total_points = QuizSubmissionPointSystem.objects.filter(
            user_id=obj.id
        ).aggregate(total_points=Sum("points_earned"))["total_points"]
        return total_points or 0

    def get_total_points_earned_for_assignments(self, obj):
        total_points = PointSystem.objects.filter(user_id=obj.id).aggregate(
            total_points=Sum("points_earned")
        )["total_points"]
        return total_points or 0


class SendEmailResetSerializer(BaseSendEmailResetSerializer):
    class Meta(BaseSendEmailResetSerializer):
        fields = ("email",)


class PasswordResetConfirmSerializer(BasePasswordResetConfirmSerializer):
    class Meta(BasePasswordResetConfirmSerializer):
        fields = ("new_password", "re_new_password")


class InstructorSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = Instructor
        fields = ["id", "email", "first_name", "last_name"]


# course category serializer
class CategorySerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()
    total_course = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "category_img",
            "courses",
            "total_course",
        ]

    def get_courses(self, cat: Category):
        return cat.courses_set.values(
            "id", "name", "description", "duration", "course_img"
        ).all()

    def get_total_course(self, total: Category):
        return total.courses_set.count()


# Course serializers
class CourseRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRequirement
        fields = "__all__"

    # def get_lessons(self, lessons: Module):
    #     return lessons.contentupload_set.values('id','content','content_title','content_description','date_uploaded','date_updated')

    # instructor = InstructorSerializer()
    # lessons = GetContentUploadSerializer()
    # lessons = serializers.SerializerMethodField()
    # total_content = serializers.SerializerMethodField()


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    total_enrolled_student = serializers.SerializerMethodField()
    module = serializers.SerializerMethodField()
    # total_content = serializers.SerializerMethodField()
    # module = serializers.SerializerMethodField()
    # lessons = serializers.SerializerMethodField()

    class Meta:
        model = Courses
        fields = [
            "id",
            "category",
            # "instructor",
            "course_img",
            "name",
            "description",
            "duration",
            "requirements1",
            "requirements2",
            "requirements3",
            "requirements4",
            "requirements5",
            "set_start_date",
            "is_started",
            "price",
            "promotion_price",
            "discounts",
            "price_override",
            "uploaded",
            "updated",
            "view_counter",
            "total_enrolled_student",
            "module",
            # "total_content",
            # "lessons",
        ]

    # def get_price_override(self, obj):
    #     try:
    #         promo = Promotion.courses_on_promotion.through.objects.filter(Q(promotion_id__is_active=True) & Q(course_id=obj.id)).select_related('promotion','course')
    #         for x in promo:
    #             return x.price_override
    #     except Exception as err:
    #         # print('Failed: ', err)
    #         return False

    # def get_discounts(self, obj):
    #     try:
    #         promo = Promotion.courses_on_promotion.through.objects.filter(Q(promotion_id__is_active=True) & Q(course_id=obj.id)).select_related('promotion','course')
    #         for x in promo:
    #             return f'{x.promotion.promo_reduction}%'
    #     except Exception as err:
    #         # print('Failed: ', err)
    #         return None

    # def get_promotion_price(self, obj):
    #     try:
    #         promo = Promotion.courses_on_promotion.through.objects.filter(Q(promotion_id__is_active=True) & Q(course_id=obj.id)).select_related('promotion','course')
    #         for x in promo:
    #             return x.promo_price
    #     except Exception as err:
    #         # print('Failed: ', err)
    #         return None

    def get_total_enrolled_student(self, student: Courses):
        return student.enrollment_set.count()

    def get_module(self, course: Courses):
        modules = course.modules_set.all()
        serialized_modules = ModuleSerializer(modules, many=True).data
        return serialized_modules

    # def get_total_content(self, student: Courses):
    #     return student.contentupload_set.count()

    # def get_module(self, module: Courses):
    #     return module.modules_set.values('id','module_name','lessons')

    # def get_lessons(self, lessons: Courses):
    #     return lessons.contentupload_set.values('id','content', "module",'content_title','content_description','date_uploaded','date_updated')


# class ModuleSerializer(serializers.ModelSerializer):
#     lessons = serializers.SerializerMethodField()
#     class Meta:
#         model = Module
#         fields = ["id", "name", "description", "lessons"]

#     def get_lessons(self, lessons: Module):
#         return lessons.contentupload_set.values('id','content','content_title','content_description','date_uploaded','date_updated')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message", "date_added"]


# Course serializers
class CreateCourseSerializer(serializers.ModelSerializer):
    # instructor = InstructorSerializer()
    class Meta:
        model = Courses
        fields = [
            "id",
            "category",
            "name",
            "course_img",
            "duration",
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

    def save(self, **kwargs):
        category = self.validated_data["category"]
        name = self.validated_data["name"]
        course_img = self.validated_data["course_img"]
        duration = self.validated_data["duration"]
        description = self.validated_data["description"]
        requirements1 = self.validated_data["requirements1"]
        requirements2 = self.validated_data["requirements2"]
        requirements3 = self.validated_data["requirements3"]
        requirements4 = self.validated_data["requirements4"]
        requirements5 = self.validated_data["requirements5"]
        price = self.validated_data["price"]
        new_course = Courses.objects.create(
            category=category,
            name=name,
            description=description,
            duration=duration,
            course_img=course_img,
            requirements1=requirements1,
            requirements2=requirements2,
            requirements3=requirements3,
            requirements4=requirements4,
            requirements5=requirements5,
            price=price,
        )
        update_course_email(category, name, description, requirements1)
        return new_course


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
    courses_id = serializers.IntegerField()

    class Meta:
        model = Enrollment
        fields = ["id", "courses_id", "interval", "date_enrolled", "completion_status"]

    def validate_courses_id(self, value):
        return validate_id(Courses, value)


class UpdateEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "update_enrollment_serializer"
        model = Enrollment
        fields = ["id", "completion_status"]


class CertificateSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    certificate_url = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        fields = "__all__"

    def get_full_name(self, obj):
        return f"{obj.enrollment.student.user.get_full_name()}"

    def get_certificate_url(self, obj):
        return f"enrollment/{obj.enrollment_id}/certificate/{obj.id}/pdf/"




# content upload management
class GetContentUploadSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    quiz = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = ContentUpload
        fields = [
            "id",
            "user",
            "quiz",
            "content",
            "content_title",
            "content_description",
            "date_uploaded",
            "date_updated",
        ]


# content upload management
# class GetContentUploadSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()
#     class Meta:
#         model = ContentUpload
#         fields = [
#             "id",
#             "user",
#             "content",
#             "content_title",
#             "content_description",
#             "date_uploaded",
#             "date_updated",
#         ]

#     def get_user(self, obj):
#         return obj.user.username


class GetContentUploadSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    quiz = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = ContentUpload
        fields = [
            "id",
            "user",
            "content",
            "quiz",
            "content_title",
            "content_description",
            "date_uploaded",
            "date_updated",
        ]

    def get_user(self, obj):
        return obj.user.username


from quiz.serializers import QuestionSerializer


class ContentUploadSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    # module = ModuleSerializer()
    quiz = QuestionSerializer(many=True)

    class Meta:
        model = ContentUpload
        fields = [
            "id",
            "user",
            "quiz",
            "content",
            "content_title",
            "content_description",
            "date_uploaded",
            "date_updated",
        ]

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User with the given ID does not exist")

    def save(self, *args, **kwargs):
        user = self.validated_data["user"]
        content = self.validated_data["content"]
        content_title = self.validated_data["content_title"]
        content_description = self.validated_data["content_description"]
        date_uploaded = self.validated_data["date_uploaded"]
        content_uploads_mail = ContentUpload.objects.create(
            user=user,
            content=content,
            content_title=content_title,
            content_description=content_description,
        )
        send_content_upload_mail(content, content_title, content_description, user)
        return content_uploads_mail


# class ModuleSerializer(serializers.ModelSerializer):
#     lessons = GetContentUploadSerializer(many=True)



class ModuleSerializer(serializers.ModelSerializer):
    lessons = GetContentUploadSerializer(many=True)

    # quiz= QuestionSerializer(many=True)
    class Meta:
        model = Modules
        fields = [
            "id",
            "module_name",
            "is_starting_at",
            "is_ending_at",
            "is_active",
            "is_approved",
            "lessons",
            "date_uploaded",
            "date_updated",
        ]
        # fields = ["id", "module_name","is_starting_at","is_ending_at","is_active","is_approved","lessons", "quiz","date_uploaded","date_updated"]


# class GetContentManagementSerializer(serializers.ModelSerializer):
#     # course = serializers.SerializerMethodField()
#     content_uploads = serializers.SerializerMethodField()
#     user = serializers.CharField(source="user.username")

#     class Meta:
#         model = ContentManagement
#         fields = [
#             "id",
#             "user",
#             "course_id",
#             "content_uploads",
#             "date_uploaded",
#             "date_updated",
#         ]

#     def get_content_uploads(self, obj):
#         return obj.content_uploads.values(
#             "id",
#             "user__username",
#             "content",
#             "content_title",
#             "content_description",
#             "date_uploaded",
#             "date_updated",
#         )

#     # def get_course(self, obj):
#     #     return obj.course.name


# class ContentManagementSerializer(serializers.ModelSerializer):
#     course_id = serializers.IntegerField()
#     class Meta:
#         model = ContentManagement
#         fields = ["id", "course_id", "date_uploaded", "date_updated"]

#     def validate_course_id(self, value):
#         if not Courses.objects.filter(id=value).exists():
#             raise serializers.ValidationError("Course with the given ID does not exist")
#         return value

#     def create(self, validated_data):
#         course_id = validated_data["course_id"]
#         content_management = ContentManagement.objects.create(
#             course_id=course_id, **validated_data
#         )

#         return content_management

#     def save(self, **kwargs):
#         course_id = self.validated_data["course_id"]


#         try:
#             content_management = ContentManagement.objects.create(course_id=course_id)
#             for x in content_uploads:
#                 content_uploads, _ = ContentUpload.objects.get_or_create(**x)
#                 content_management.content_uploads.add(content_uploads)

#             content_management.save()
#             return content_management
#         except Exception as e:
#             print("Error saving content-management endpoints", e)


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
            return serializers.ValidationError(
                "The course ID you are trying to get isn't available"
            )
        raise value


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "question_bank",
            "student",
            "text",
            "question_type",
            "created_at",
            "updated_at",
        ]


class ChoicesSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True, required=True)

    class Meta:
        model = Choice
        fields = ["question", "text", "is_correct"]


class AssessmentSerialier(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = [
            "course",
            "questions",
            "title",
            "descrpition",
            "time_limit",
            "created_at",
            "updated_at",
        ]


class SubmissionSerializer(serializers.ModelSerializer):
    assessment = AssessmentSerialier(many=True, required=True)
    course = CourseSerializer()

    class Meta:
        model = Submission
        fields = ["assessment", "user", "submitted_at"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            "submission",
            "student",
            "question",
            "text",
            "selected_choice",
            "is_correct",
            "points",
        ]


class GradingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grading
        fields = ["assessment", "student", "score", "feedback"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        ref_name = "Profile"


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
        fields = ("id", "first_name", "last_name", "username", "email", "is_staff")


class CourseEventSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField()

    class Meta:
        model = CourseEvent
        fields = (
            "id",
            "user",
            "course_id",
            "event_text",
            "start_date",
            "end_date",
            "calendar_event_id",
        )
        read_only_fields = ("user",)

    def validate_course_id(self, value):
        return validate_id(Courses, value)


# class CourseRatingSerializer(serializers.ModelSerializer):
#     class Meta:
#         models = CourseRating
#         fields = "__all__"

# class GetCourseRatingSerializer(serializers.ModelSerializer):
#     cou
#     class Meta:
#         models = CourseRating
#         fields = "__all__"


class CourseRatingSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField()

    class Meta:
        model = CourseRating
        fields = ("id", "course_id", "value")
        # validators = [ UniqueTogetherValidator(
        #     queryset=CourseRating.objects.all(),
        #     fields=['user_id', 'course_id'])
        # ]

    def validate_course_id(self, value):
        if not Courses.objects.filter(id=value).exists():
            raise serializers.ValidationError("Course id does not exist")
        return value


class GetCourseRatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    course = serializers.StringRelatedField()

    class Meta:
        model = CourseRating
        fields = "__all__"
