from django.contrib import admin

from .models import *


@admin.register(ForumQuestion)
class ForumQuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "course", "title", "date_posted", "date_changed"]
    list_filter = ["date_posted", "date_changed"]


@admin.register(ForumAnswer)
class ForumAnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "forum_question", "date_posted", "date_changed"]
    list_filter = ["date_posted", "date_changed"]


@admin.register(Upvote)
class UpvoteAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "forum_question", "value"]


@admin.register(UpvoteAnswer)
class UpvoteAnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "forum_answer", "value"]
