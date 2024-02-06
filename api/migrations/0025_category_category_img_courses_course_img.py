# Generated by Django 4.2.9 on 2024-02-05 20:09

import django.core.validators
from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0024_alter_courses_requirements1_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="category_img",
            field=models.FileField(
                blank=True,
                default="category.jpg",
                null=True,
                upload_to="category",
                validators=[
                    utils.validators.validate_file_size,
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["png", "jpg", "svg", "webp"]
                    ),
                ],
            ),
        ),
        migrations.AddField(
            model_name="courses",
            name="course_img",
            field=models.FileField(
                blank=True,
                default="course.jpg",
                null=True,
                upload_to="course",
                validators=[
                    utils.validators.validate_file_size,
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["png", "jpg", "svg", "webp"]
                    ),
                ],
            ),
        ),
    ]