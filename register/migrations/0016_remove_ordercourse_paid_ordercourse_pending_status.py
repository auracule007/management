# Generated by Django 4.2.9 on 2024-02-07 10:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("register", "0015_payment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ordercourse",
            name="paid",
        ),
        migrations.AddField(
            model_name="ordercourse",
            name="pending_status",
            field=models.CharField(
                choices=[("P", "Pending"), ("C", "Complete"), ("F", "Failed")],
                default="P",
                max_length=50,
            ),
        ),
    ]
