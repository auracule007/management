from django.db import models
from django.contrib.auth.models import AbstractUser
from . validators import validate_file_size
from django.core.validators import MinValueValidator, FileExtensionValidator

# Create your models here.
class User(AbstractUser):
    Student = 'Student'
    Instructor = 'Instructor'

    USER_TYPE_CHOICES = [
        (Student, 'Student'),
        (Instructor, 'Instructor'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='Student')
    profile_img = models.FileField(upload_to='profile', default='profile.jpg', validators= [
        validate_file_size, FileExtensionValidator(allowed_extensions=['png', 'jpg', 'svg', 'webp'])
    ])
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)

    
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name 

class Courses(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, blank=True)
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
    student = models.ForeignKey(Student, on_delete= models.CASCADE)
    courses = models.ForeignKey(Courses, on_delete= models.CASCADE)
    date_enrolled = models.DateField(auto_now=True)


class CourseManagement(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete= models.CASCADE)
    courses = models.ForeignKey(Courses, on_delete= models.CASCADE)
    course_doc = models.FileField(upload_to='course_doc', default='course_doc.jpg', validators= [
        validate_file_size, FileExtensionValidator(allowed_extensions=['png', 'jpg', 'svg', 'webp'])
    ])
    course_video = models.FileField(upload_to='course_doc', default='course_doc.mp4', validators= [
        validate_file_size, FileExtensionValidator(allowed_extensions=['mp4', 'mkv', 'webm', 'avi'])
    ])


