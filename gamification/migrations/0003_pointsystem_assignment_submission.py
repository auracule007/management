# Generated by Django 4.2.9 on 2024-01-29 12:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0010_remove_assignment_is_completed_and_more"),
        ("gamification", "0002_remove_pointsystem_assignment"),
    ]

    operations = [
        migrations.AddField(
            model_name="pointsystem",
            name="assignment_submission",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="quiz.assignmentsubmission",
            ),
        ),
    ]
