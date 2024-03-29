from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import IntegrityError, models, transaction

from api.models import Courses, Instructor, Student, User

from performance.models import UserPerformance, UserQuizPerformance
from utils.choices import *
from utils.validators import validate_file_size


# Assignment
class Assignment(models.Model):
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, blank=True, null=True
    )
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, blank=True, null=True)
    assignment_title = models.CharField(max_length=250)
    assignment_description = models.TextField()
    assignment_doc = models.FileField(
        upload_to="assignment",
        validators=[
            validate_file_size,
            FileExtensionValidator(
                allowed_extensions=[
                    "png",
                    "jpg",
                    "svg",
                    "webp",
                    "pdf",
                    "docx",
                    "xlsx",
                    "doc",
                    "xls",
                ]
            ),
        ],
        blank=True,
        null=True,
    )
    is_ended = models.BooleanField(default=False)
    date_given = models.DateTimeField()
    date_to_be_submitted = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date_created",)

    def __str__(self):
        return f"Assignment::{self.assignment_title}"


class AssignmentSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    assignment_submission_doc = models.FileField(
        upload_to="assignment",
        validators=[
            validate_file_size,
            FileExtensionValidator(
                allowed_extensions=[
                    "png",
                    "jpg",
                    "svg",
                    "webp",
                    "pdf",
                    "docx",
                    "xlsx",
                    "doc",
                    "xls",
                ]
            ),
        ],
        blank=True,
        null=True,
    )
    submission_context = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    points = models.PositiveIntegerField(default=0)
    date_submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date_submitted",)

    def __str__(self):
        return f"{self.user}:::{self.assignment.assignment_title}"

    def __init__(self, *args, **kwargs):
        super(AssignmentSubmission, self).__init__(*args, **kwargs)
        self._original_is_completed = self.is_completed

    def save(self, *args, **kwargs):
        try:

            if not self.pk:
                if self.is_completed:
                    self.points += 1
                    self.update_user_performance()
            else:
                if self.is_completed and not self._original_is_completed:
                    self.points += 1
                    self.update_user_performance()

                elif not self.is_completed and self._original_is_completed:
                    self.points -= 1
                    self.update_user_performance()
            super(AssignmentSubmission, self).save(*args, **kwargs)
            self._original_is_completed = self.is_completed
        except Exception as e:
            print(
                "Error while saving assignment submission and incrementing the points: ",
                e,
            )

    def update_user_performance(self):
        try:
            user_id = self.user_id
            user_performance, _ = UserPerformance.objects.get_or_create(user_id=user_id)
            user_performance.calculate_overall_performance_percentage(user_id)
            user_performance.update_performance_percentage(user_id)
            user_performance.save()
        except Exception as e:
            print("Integrity error occurred:", e)

# ASSIGNMENT SUBMISSION
    
class PointForEachAssignmentSubmission(models.Model):
    
    assignment_submission = models.ForeignKey(AssignmentSubmission, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user}'

class GemForEachPointAssignmentSubmission(models.Model):
    point_for_each_assignment_submission = models.ForeignKey(PointForEachAssignmentSubmission, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user}'

class CoinAssignmentSubmission(models.Model):
    gems = models.ForeignKey(GemForEachPointAssignmentSubmission, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user}'

class TokenAssignmentSubmission(models.Model):
    coin = models.ForeignKey(CoinAssignmentSubmission, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user}'
    
    
# Quiz
class QuestionCategory(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.instructor}::{self.name}"

    class Meta:
        ordering = ["-id"]


class QuizQuestion(models.Model):
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, related_name="instructor"
    )
    title = models.CharField(max_length=255, verbose_name="Quiz Title")
    category = models.ForeignKey(QuestionCategory, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.title}"


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
        max_length=100,
    )
    title = models.CharField(max_length=255, verbose_name=("Ask question"))
    difficulty = models.CharField(
        choices=SCALE,
        default="Fundamental",
        verbose_name=("Difficulty"),
        max_length=100,
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
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="student_answer",
        blank=True,
        null=True,
    )
    question = models.ForeignKey(
        Question, related_name="answer_question", on_delete=models.DO_NOTHING
    )
    answer_text = models.CharField(max_length=255, verbose_name=("Answer Text"))
    is_correct = models.BooleanField(default=False)
    points = models.PositiveIntegerField(default=0)
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


class QuizSubmission(models.Model):
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, blank=True, null=True
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, blank=True, null=True
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    are_answers = models.ManyToManyField(Answer)
    is_completed = models.BooleanField(default=False)
    points_earned = models.PositiveIntegerField(default=0)
    submitted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username}::{self.question.title}"
    

    def __init__(self, *args, **kwargs):
        super(QuizSubmission, self).__init__(*args, **kwargs)
        self._original_is_completed = self.is_completed

    def save(self, *args, **kwargs):
        try:
            if not self.pk:
                if self.is_completed:
                    self.points += 1
                    self.update_user_quiz_performance()
            else:
                if self.is_completed and not self._original_is_completed:
                    self.points += 1
                    self.update_user_quiz_performance()

                elif not self.is_completed and self._original_is_completed:
                    self.points -= 1
                    self.update_user_quiz_performance()
            super(QuizSubmission, self).save(*args, **kwargs)
            self._original_is_completed = self.is_completed
        except Exception as e:
            print(
                "Error while saving assignment submission and incrementing the points: ",
                e,
            )

    def update_user_quiz_performance(self):
        try:
            user_id = self.user_id
            user_performance, _ = UserQuizPerformance.objects.get_or_create(user_id=user_id)
            user_performance.calculate_overall_quiz_performance_percentage(user_id)
            user_performance.update_performance_percentage(user_id)
            user_performance.save()
        except Exception as e:
            print("Integrity error occurred:", e)


class PointForEachQuizSubmission(models.Model):
    
    quiz_submission = models.ForeignKey(QuizSubmission, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user}'

class GemForEachPointQuizSubmission(models.Model):
    point_for_each_quiz_submission = models.ForeignKey(PointForEachQuizSubmission, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user}'

class CoinQuizSubmission(models.Model):
    gems = models.ForeignKey(GemForEachPointQuizSubmission, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user}'

class TokenQuizSubmission(models.Model):
    coin = models.ForeignKey(CoinQuizSubmission, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user}'
    


class AwardForAssignmentSubmission(models.Model):
    assignment_submission = models.ForeignKey(
        AssignmentSubmission, on_delete=models.CASCADE
    )
    award_name = models.CharField(max_length=255)
    issue_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assignment_submission}"


class AwardForQuizSubmission(models.Model):
    quiz_submission = models.ForeignKey(QuizSubmission, on_delete=models.CASCADE)
    award_name = models.CharField(max_length=255)
    issue_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quiz_submission}"
