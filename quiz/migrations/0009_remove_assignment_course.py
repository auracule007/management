# Generated by Django 4.2.9 on 2024-01-29 12:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0008_assignment_course_assignment_instructor"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="assignment",
            name="course",
        ),
    ]
