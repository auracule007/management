# Generated by Django 4.2.9 on 2024-02-04 12:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("register", "0006_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cartcoursesitem",
            name="cartcourses",
        ),
        migrations.RemoveField(
            model_name="cartcoursesitem",
            name="course",
        ),
        migrations.RemoveField(
            model_name="ordercourse",
            name="cartcoursesitem",
        ),
        migrations.RemoveField(
            model_name="ordercourse",
            name="courses",
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="ordercourse",
        ),
        migrations.RemoveField(
            model_name="payment",
            name="course",
        ),
        migrations.RemoveField(
            model_name="payment",
            name="orderitem",
        ),
        migrations.RemoveField(
            model_name="payment",
            name="user",
        ),
        migrations.DeleteModel(
            name="CartCourses",
        ),
        migrations.DeleteModel(
            name="CartCoursesItem",
        ),
        migrations.DeleteModel(
            name="OrderCourse",
        ),
        migrations.DeleteModel(
            name="OrderItem",
        ),
        migrations.DeleteModel(
            name="Payment",
        ),
    ]
