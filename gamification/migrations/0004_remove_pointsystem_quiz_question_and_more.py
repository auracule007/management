# Generated by Django 4.2.9 on 2024-01-30 00:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0011_remove_question_points_answer_points_quizsubmission"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("gamification", "0003_pointsystem_assignment_submission"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pointsystem",
            name="quiz_question",
        ),
        migrations.CreateModel(
            name="QuizSubmissionPointSystem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("points_earned", models.PositiveIntegerField(default=0)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                (
                    "quiz_submission",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="quiz.quizsubmission",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
