from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_file_size
from django.core.validators import MinValueValidator, FileExtensionValidator


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


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Courses(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    requirements1 = models.CharField(max_length=255)
    requirements2 = models.CharField(max_length=255)
    requirements3 = models.CharField(max_length=255)
    requirements4 = models.CharField(max_length=255)
    requirements5 = models.CharField(max_length=255)
    price = models.IntegerField()
    uploaded = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class CourseReview(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    body = models.TextField()
    date = models.DateTimeField(auto_now=True)


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now=True)


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


class ContentUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.FileField(
        upload_to="content/",
        validators=[
            validate_file_size,
            FileExtensionValidator(
                allowed_extensions=[
                    "mp4",
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
    )
    content_title = models.CharField(max_length=250)
    content_description = models.TextField(blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"content: {self.content_title}"


class ContentManagement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    content_uploads = models.ManyToManyField(ContentUpload)
    is_approved = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.course.name}"


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
        return f"{self.course.name}"


class Question(models.Model):
    QUESTION_CHOICES = [("multiple_choice", "Multiple Choice"), ("essay", "Essay")]
    question_bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=50, choices=QUESTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.question_bank.course}"


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
