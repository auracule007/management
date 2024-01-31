# Generated by Django 4.2.9 on 2024-01-27 17:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0020_enrollment_completion_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="CourseViewCount",
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
                ("count", models.PositiveIntegerField(default=0)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.courses"
                    ),
                ),
            ],
        ),
    ]
