from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["id", "first_name", "last_name", "username", "email"]
    ordering = ['-id']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "user_type",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )


admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(ContentUpload)
admin.site.register(ContentManagement)
admin.site.register(Enrollment)
admin.site.register(Courses)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(QuestionBank)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Assessment)
admin.site.register(Submission)
admin.site.register(Answer)
admin.site.register(Grading)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "message", "is_read"]
    list_editable = ["is_read"]
