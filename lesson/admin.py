from django.contrib import admin

from api.models import ContentUpload

from .models import *

admin.site.register(CourseUserProgress)

# class ContentUploadInline(admin.TabularInline):
#   model = ContentUpload


# @admin.register(CourseUserProgress)
# class CourseUserProgressAdmin(admin.ModelAdmin):
#   inlines = [ContentUploadInline]
#   list_display = ['id', 'user', 'course_progress_percentage']

# admin.site.register(ContentUpload)
