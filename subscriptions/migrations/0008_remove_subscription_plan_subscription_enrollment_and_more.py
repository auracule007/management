# Generated by Django 4.2.9 on 2024-02-17 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0035_enrollment_interval"),
        ("subscriptions", "0007_subscription_transaction_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscription",
            name="plan",
        ),
        migrations.AddField(
            model_name="subscription",
            name="enrollment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.enrollment",
            ),
        ),
        migrations.AlterField(
            model_name="plan",
            name="interval",
            field=models.CharField(
                choices=[
                    ("Weekly", "Weekly"),
                    ("Monthly", "Monthly"),
                    ("Yearly", "Yearly"),
                ],
                default="weekly",
                help_text="weekly, monthly, yearly",
                max_length=20,
            ),
        ),
    ]
