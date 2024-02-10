# Generated by Django 4.2.9 on 2024-02-08 11:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscription",
            name="stripe_subscription_id",
        ),
        migrations.AlterField(
            model_name="plan",
            name="name",
            field=models.CharField(
                choices=[("Gold", "Gold"), ("Silver", "Silver")], max_length=255
            ),
        ),
    ]
