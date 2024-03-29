from django.contrib.auth.models import AbstractUser
from django.core.validators import (FileExtensionValidator, MaxValueValidator,
                                    MinValueValidator)
from django.db import models
from django.urls import reverse

from utils.choices import PLAN_CHIOCES, SCALE
from django.db.models import Q
from utils.validators import validate_file_size


# Create your models here.
class User(AbstractUser):
    Student = "Student"
    Instructor = "Instructor"

    USER_TYPE_CHOICES = [
        (Student, "Student"),
        (Instructor, "Instructor"),
    ]

    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default="Student"
    )
    profile_img = models.FileField(
        upload_to="profile",
        default="profile.jpg",
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=["png", "jpg", "svg", "webp"]),
        ],
    )
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user}::{self.first_name} {self.last_name}"


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)

    def __str__(self):
        if self.full_name == "" or self.full_name == None:
            return self.user.username
        return self.full_name


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category_img = models.FileField(
        upload_to="category",
        default="category.jpg",
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=["png", "jpg", "svg", "webp", "jpeg"]),
        ], null=True, blank=True
    )

    def __str__(self):
        return self.name


class Courses(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=255)
    course_img = models.FileField(
        upload_to="course",
        default="course.jpg",
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=["png", "jpg", "svg", "webp", "jpeg"]),
        ], null=True, blank=True
    )
    description = models.TextField()
    duration = models.CharField(max_length=255, null= True, blank=True)
    requirements1 = models.CharField(max_length=255, null= True, blank=True)
    requirements2 = models.CharField(max_length=255, null= True, blank=True)
    requirements3 = models.CharField(max_length=255, null= True, blank=True)
    requirements4 = models.CharField(max_length=255, null= True, blank=True)
    requirements5 = models.CharField(max_length=255, null= True, blank=True)
    difficulty = models.CharField(
        choices=SCALE,
        default="Fundamental",
        verbose_name=("Difficulty"),
        max_length=100,
    )
    set_start_date = models.DateField(blank=True,null=True)
    is_started = models.BooleanField(default=False)
    price = models.IntegerField(default=100.00)
    uploaded = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        try:
            return reverse("courses-detail", args=[self.pk])
        except Exception as e:
            print("ERROR WHILE GETING ABSOLUTE URL: ", e)

    @property
    def price_override(self):
        try:
            from promotion.models import Promotion
            promo = Promotion.courses_on_promotion.through.objects.filter(Q(promotion_id__is_active=True) & Q(course_id=self.id)).select_related('promotion','course')
            for x in promo:
                return x.price_override
        except Exception as err:
            # print('Failed: ', err)
            return False
    
    @property
    def discounts(self):
        try:
            from promotion.models import Promotion
            promo = Promotion.courses_on_promotion.through.objects.filter(Q(promotion_id__is_active=True) & Q(course_id=self.id)).select_related('promotion','course')
            for x in promo:
                return f'{x.promotion.promo_reduction}%'
        except Exception as err:
            # print('Failed: ', err)
            return None

    @property  
    def promotion_price(self):
        try:
            from promotion.models import Promotion
            promo = Promotion.courses_on_promotion.through.objects.filter(Q(promotion_id__is_active=True) & Q(course_id=self.id)).select_related('promotion','course')
            for x in promo:
                return x.promo_price
        except Exception as err:
            # print('Failed: ', err)
            return None
        
    @property
    def view_counter(self):
        try:
            view_count = self.courseviewcount_set.get(course_id=self.id)
            if view_count.count < 1000:
                return view_count.count
            elif view_count.count < 1000000:
                view_count.count = view_count.count / 1000
                return f"{view_count.count:.1f}k"
            else:
                view_count.count = view_count.count / 1000000
                return f"{view_count.count:.1f}M"
        except Exception as e:
            print("Error while counting views: ", e)
            return 0


class CourseRequirement(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    requirement_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course.name
    

class CourseViewCount(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"View count for {self.course.name}"


class CourseReview(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    body = models.TextField()
    date = models.DateTimeField(auto_now=True)


class CourseRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.user.username} rating for {self.course.name}"

    class Meta:
        unique_together = ["user", "course"]


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
    interval = models.CharField(max_length=20, help_text='weekly, monthly, yearly', choices=PLAN_CHIOCES, default='weekly')
    completion_status = models.BooleanField(default=False)
    date_enrolled = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.courses.name} - {self.student.first_name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.completion_status and not hasattr(self, 'certificate'):
            certificate_number = f"{self.courses.name[:3].upper()}-{self.student.id}-{self.id}"
            Certificate.objects.create(enrollment=self, certificate_number=certificate_number)

from django.db.models import Count

class Certificate(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    certificate_number = models.CharField(max_length=100, unique=True)
    issue_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.enrollment.student.user.first_name} - {self.enrollment.student.user.last_name}'
    
    @classmethod
    def get_certificate_count(cls, user):
        return cls.objects.filter(enrollment__student__user=user).count()


    
class CourseManagement(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
    course_doc = models.FileField(
        upload_to="course_doc",
        default="course_doc.jpg",
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=["png", "jpg", "svg", "webp"]),
        ],
    )
    course_video = models.FileField(
        upload_to="course_doc",
        default="course_doc.mp4",
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=["mp4", "mkv", "webm", "avi"]),
        ],
    )
# class Module(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     is_starting_at = models.DateTimeField(blank=True, null=True)
#     is_ending_at = models.DateTimeField(blank=True, null=True)
#     is_active = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
#     date_updated = models.DateField(auto_now=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         ordering = ('date_created',)
from quiz.models import *
class ContentUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ManyToManyField(Question)
    # module = models.ForeignKey(Module, on_delete=models.CASCADE, blank=True, null=True)
    # course = models.ForeignKey(Courses, on_delete=models.CASCADE, blank=True, null=True)
    content = models.FileField(
        upload_to="content/course",
        validators=[
            validate_file_size,
            FileExtensionValidator(
                allowed_extensions=[
                    "mp4",
                    "jpeg",
                    "mkv",
                    "webm",
                    "avi",
                    "pdf",
                    "txt",
                    "jpg",
                    "png",
                    "docx",
                    "xlsx",
                    "doc",
                ]
            ),
        ],
        blank=True,
        null=True,
    )
    content_title = models.CharField(max_length=250)
    content_description = models.TextField(blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"content: {self.content_title}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    ["name", "email", "subject", "message", "date_added"]
    def __str__(self):
        return self.name


from quiz.models import *
class Modules(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, blank=True, null=True)
    module_name = models.CharField(max_length=255)
    lessons = models.ManyToManyField(ContentUpload)
    # quiz = models.ManyToManyField(Question)
    is_starting_at = models.DateTimeField(blank=True, null=True)
    is_ending_at = models.DateTimeField(blank=True,null=True)
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.module_name}"





class ModulesHighFive(models.Model):
    '''This is the model for creating High five for the'''

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    modules = models.ForeignKey(Modules, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f'{self.user}'



class PointForEachModule(models.Model):
    modules_high_five = models.ForeignKey(Modules, on_delete=models.CASCADE, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user}'


class GemForEachPoint(models.Model):
    point_for_each_module = models.ForeignKey(PointForEachModule, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user}'

class Coin(models.Model):
    gems = models.ForeignKey(GemForEachPoint, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user}'

class Token(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user}'

# chat models
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    message = models.CharField(max_length=1000)
    is_read = models.BooleanField(default=False)
    date_messaged = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date_messaged"]

    def __str__(self):
        return f"{self.sender} - {self.receiver}"

    @property
    def sender_profile(self):
        sender_profile = Profile.objects.get(user=self.sender)

    @property
    def receiver_profile(self):
        receiver_profile = Profile.objects.get(user=self.receiver)


class QuestionBank(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    course = models.ManyToManyField(Courses)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"


class Question(models.Model):
    QUESTION_CHOICES = [("multiple_choice", "Multiple Choice"), ("essay", "Essay")]
    question_bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=50, choices=QUESTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.question_bank.name}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text}"


class Assessment(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    title = models.CharField(max_length=255)
    description = models.TextField()
    time_limit = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class Submission(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assessment}"


class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    selected_choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE, null=True, blank=True
    )
    is_correct = models.BooleanField(null=True, blank=True)
    points = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.student}"


class Grading(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.FloatField()
    feedback = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Assessment::{self.assessment.title}::{self.student.user.username}"


# EVENTS
class CourseEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    event_text = models.CharField(max_length=250)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    calendar_event_id = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"CourseEvent::{self.course.name}::{self.user.username}"

    class Meta:
        ordering = ["-start_date"]


# class Code(models.Model):
#     LANGUAGE = (
#         ('PYTHON3', 'PYTHON3'),
#         ('JAVA', 'JAVA'),
#         ('JAVASCRIPT', 'JAVASCRIPT'),
#         ('SCRATCH', 'SCRATCH'),
#     )
#     title = models.CharField(max_length=255, blank=True, null=True)
#     program_language = models.CharField(max_length=50, choices=LANGUAGE)
#     program_code = models.TextField()
#     created_at = models.DateField(auto_now_add=True)
