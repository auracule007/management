# Generated by Django 4.2.9 on 2024-03-09 13:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0016_remove_question_is_completed_and_more"),
        ("api", "0041_modules_quiz"),
    ]

    operations = [
        migrations.AddField(
            model_name="contentupload",
            name="quiz",
            field=models.ManyToManyField(to="quiz.question"),
        ),
    ]
