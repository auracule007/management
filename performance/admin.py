from django.contrib import admin

from .models import *

admin.site.register(UserPerformance)
admin.site.register(UserPerformanceForModuleCompletion)
admin.site.register(GemForEachPoint)
admin.site.register(Coin)
admin.site.register(Token)
admin.site.register(ModulesHighFive)