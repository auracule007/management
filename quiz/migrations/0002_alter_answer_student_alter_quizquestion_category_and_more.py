# Generated by Django 4.2.9 on 2024-01-24 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0016_courseevent_calendar_event_id"),
        ("quiz", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="student",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="student_answer",
                to="api.student",
            ),
        ),
        migrations.AlterField(
            model_name="quizquestion",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="quiz.questioncategory",
            ),
        ),
        migrations.AlterField(
            model_name="quizquestion",
            name="title",
            field=models.CharField(max_length=255, verbose_name="Quiz Title"),
        ),
    ]
