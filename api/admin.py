from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from api.tasks import check_course_start_date

from .models import *


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["id", "first_name", "last_name", "username", "email"]
    ordering = ["-id"]
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
admin.site.register(ContentUpload)
admin.site.register(Module)
# admin.site.register(ContentManagement)
admin.site.register(Enrollment)
# admin.site.register(Module)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(QuestionBank)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Assessment)
admin.site.register(Submission)
admin.site.register(Answer)
admin.site.register(Grading)
admin.site.register(CourseEvent)
admin.site.register(CourseRating)
admin.site.register(CourseViewCount)
admin.site.register(CourseRequirement)

@admin.register(Courses)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','is_started']

    def save_model(self, request,obj, form,change):
        super().save_model(request,obj,form,change)
        check_course_start_date.delay()

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "message", "is_read"]
    list_editable = ["is_read"]
