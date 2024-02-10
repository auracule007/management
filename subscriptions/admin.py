from django.contrib import admin
from .models import *
admin.site.register(Plan)
from .tasks import check_sub_expiration

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
  list_display = ('id','user','plan','start_date','expiration_date','is_active')

  def save_model(self, request,obj, form,change):
    super().save_model(request,obj,form,change)
    check_sub_expiration.delay()

    