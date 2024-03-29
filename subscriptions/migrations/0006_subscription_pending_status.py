# Generated by Django 4.2.9 on 2024-02-13 05:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0005_alter_subscription_start_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="pending_status",
            field=models.CharField(
                choices=[("P", "Pending"), ("C", "Complete"), ("F", "Failed")],
                default="P",
                max_length=50,
            ),
        ),
    ]
