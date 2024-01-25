# Generated by Django 4.2.9 on 2024-01-25 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_alter_answer_student_alter_quizquestion_category_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['-id'], 'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.AlterModelOptions(
            name='questioncategory',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='quizquestion',
            options={'ordering': ['-id'], 'verbose_name': 'Quiz', 'verbose_name_plural': 'Quizzes'},
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Ask question'),
        ),
    ]
