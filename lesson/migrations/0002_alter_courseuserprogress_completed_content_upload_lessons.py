# Generated by Django 4.2.9 on 2024-03-03 12:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0040_certificate"),
        ("lesson", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courseuserprogress",
            name="completed_content_upload_lessons",
            field=models.ManyToManyField(blank=True, to="api.modules"),
        ),
    ]
