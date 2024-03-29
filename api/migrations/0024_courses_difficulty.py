# Generated by Django 4.2.9 on 2024-02-04 12:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0023_alter_contentupload_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="courses",
            name="difficulty",
            field=models.CharField(
                choices=[
                    ("Fundamental", "Fundamental"),
                    ("Beginner", "Beginner"),
                    ("Intermediate", "Intermediate"),
                    ("Advanced", "Advanced"),
                    ("Expert", "Expert"),
                ],
                default="Fundamental",
                max_length=100,
                verbose_name="Difficulty",
            ),
        ),
    ]
