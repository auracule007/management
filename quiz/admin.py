from django.contrib import admin
from .models import *


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "instructor",
        "name",
    ]


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "instructor",
        "title",
    ]


class AnswerInlineModel(admin.TabularInline):
    model = Answer
    fields = ["instructor","answer_text", "is_correct"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    
    list_display = ["id", "title", "quiz", "date_updated"]
    inlines = [
        AnswerInlineModel,
    ]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "instructor",
        "student",
        "answer_text",
        "is_correct",
        "question",
    ]