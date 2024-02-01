# Generated by Django 4.2.9 on 2024-01-31 18:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import utils.validators


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0021_courseviewcount"),
    ]

    operations = [
        migrations.AddField(
            model_name="contentupload",
            name="course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.courses",
            ),
        ),
        migrations.AlterField(
            model_name="contentupload",
            name="content",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="content/course",
                validators=[
                    utils.validators.validate_file_size,
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=[
                            "mp4",
                            "mkv",
                            "webm",
                            "avi",
                            "pdf",
                            "txt",
                            "jpg",
                            "png",
                            "docx",
                            "xlsx",
                            "doc",
                        ]
                    ),
                ],
            ),
        ),
        migrations.DeleteModel(
            name="ContentManagement",
        ),
    ]
