# Generated by Django 4.2.9 on 2024-03-26 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0044_modules_is_completed"),
        ("performance", "0003_alter_token_coin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coin",
            name="gems",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="performance.gemforeachpoint",
            ),
        ),
        migrations.AlterField(
            model_name="gemforeachpoint",
            name="point_for_each_module",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="performance.pointforeachmodule",
            ),
        ),
        migrations.AlterField(
            model_name="pointforeachmodule",
            name="modules_high_five",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.modules",
            ),
        ),
    ]
