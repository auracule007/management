# Generated by Django 4.2.9 on 2024-01-26 04:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserPerformance",
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
                (
                    "progress_percentage",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                (
                    "completion_status",
                    models.CharField(
                        choices=[
                            ("Complete", "Complete"),
                            ("Uncomplete", "Uncomplete"),
                        ],
                        default="Uncomplete",
                        max_length=50,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]