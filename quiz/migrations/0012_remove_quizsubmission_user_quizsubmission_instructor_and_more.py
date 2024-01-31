# Generated by Django 4.2.9 on 2024-01-30 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0021_courseviewcount"),
        ("quiz", "0011_remove_question_points_answer_points_quizsubmission"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quizsubmission",
            name="user",
        ),
        migrations.AddField(
            model_name="quizsubmission",
            name="instructor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.instructor",
            ),
        ),
        migrations.AddField(
            model_name="quizsubmission",
            name="student",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.student",
            ),
        ),
    ]
