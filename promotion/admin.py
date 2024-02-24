from django.contrib import admin
from .models import *
from .tasks import *

class CourseOnPromotionAdmin(admin.StackedInline):
  model = Promotion.courses_on_promotion.through
  extra = 4
  raw_id_fields = ("course",)
  # autocomplete_fields = ('course',)

@admin.register(Promotion)
class CourseListAdmin(admin.ModelAdmin):
  model = Promotion
  inlines = [CourseOnPromotionAdmin]
  autocomplete_fields = ('courses_on_promotion','promo_type','coupon')
  list_display = ('name','is_active','promo_start')

  def save_model(self, request,obj,form, change):
    super().save_model(request,obj, form, change)
    promotion_prices.delay(obj.promo_reduction, obj.id)
    promotion_management.delay()



@admin.register(PromoType)
class PromoTypeAdmin(admin.ModelAdmin):
  list_display = ('id','name')
  search_fields = ('name',)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
  list_display = ('id','name', 'coupon_code')
  search_fields = ('coupon_code','name')
  

