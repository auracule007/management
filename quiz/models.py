from django.db import models
from utils.choices import *
from api.models import Instructor, Student, Courses, User
from django.core.validators import FileExtensionValidator, MinValueValidator
from utils.validators import validate_file_size


# Assignment
class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_title = models.CharField(max_length=250)
    assignment_description = models.TextField()
    assignment_doc = models.FileField(
        upload_to="assignment",
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=["png", "jpg", "svg", "webp", "pdf",'docx',"xlsx", "doc","xls"]),
        ],
    )
    date_given = models.DateTimeField()
    date_to_be_submitted = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Assignment::{self.user.username}'

# Quiz
class QuestionCategory(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.instructor}::{self.name}"

    class Meta:
      ordering = ['-id']

class QuizQuestion(models.Model):
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, related_name="instructor"
    )
    title = models.CharField(
        max_length=255, verbose_name="Quiz Title"
    )
    category = models.ForeignKey(
        QuestionCategory, on_delete=models.DO_NOTHING
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.instructor}::{self.title}"


class Question(models.Model):
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, related_name="instructor_question"
    )
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    quiz = models.ForeignKey(
        QuizQuestion, related_name="question", on_delete=models.DO_NOTHING
    )
    technique = models.CharField(
        choices=QUESTION_CHOICE_MODE,
        default="Multiple Choice",
        verbose_name=("Question choice mode"),
        max_length=100
    )
    title = models.CharField(max_length=255, verbose_name=("Ask question"))
    difficulty = models.CharField(
        choices=SCALE, default="Fundamental", verbose_name=("Difficulty"),max_length=100
    )
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name=("Date Created")
    )
    date_updated = models.DateTimeField(verbose_name="Last Updated", auto_now=True)
    is_active = models.BooleanField(default=False, verbose_name=("Active Status"))

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ["-id"] 

    def __str__(self):
        return f"{self.instructor}::{self.title}"


class Answer(models.Model):
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, related_name="instructor_answer"
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_answer', blank=True, null=True)
    question = models.ForeignKey(
        Question, related_name="answer_question", on_delete=models.DO_NOTHING
    )
    answer_text = models.CharField(max_length=255, verbose_name=("Answer Text"))
    is_correct = models.BooleanField(default=False)
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name=("Date Created")
    )
    date_updated = models.DateTimeField(verbose_name="Last Updated", auto_now=True)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering = ["id"]

    def __str__(self):
        return self.answer_text