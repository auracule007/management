from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . models import *

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", 'user_type',"password1", "password2","first_name", "last_name"),
            },
        ),
    )

admin.site.register(Student)
admin.site.register(Instructor)