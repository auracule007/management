# Generated by Django 4.2.9 on 2024-02-04 04:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0012_remove_quizsubmission_user_quizsubmission_instructor_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="assignment",
            name="is_ended",
            field=models.BooleanField(default=False),
        ),
    ]
