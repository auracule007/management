from django.contrib import admin

from .models import *

admin.site.register(UserPerformance)
admin.site.register(UserQuizPerformance)
admin.site.register(UserPerformanceForModuleCompletion)

