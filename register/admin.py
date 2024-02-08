from django.contrib import admin
from .models import *


@admin.register(OrderCourse)
class OrderCourseAdmin(admin.ModelAdmin):
  list_display = ['id','course']