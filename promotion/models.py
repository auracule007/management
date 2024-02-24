from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from api.models import Courses

class PromoType(models.Model):
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name

class Coupon(models.Model):
  name = models.CharField(max_length=255)
  coupon_code = models.CharField(max_length=25)
  def __str__(self):
    return self.name

class Promotion(models.Model):
  name = models.CharField(max_length=255, unique=True)
  description = models.TextField(blank=True, null=True)
  promo_reduction = models.IntegerField(default=0)
  is_active = models.BooleanField(default=False)
  is_schedule = models.BooleanField(default=False)
  promo_start = models.DateField()
  promo_end = models.DateField()
  courses_on_promotion = models.ManyToManyField(Courses, through="CourseOnPromotion")
  promo_type = models.ForeignKey(PromoType, on_delete=models.CASCADE)
  coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, blank=True, null=True)
  def __str__(self):
    return self.name
  def clean(self):
    if self.promo_start > self.promo_end:
      raise ValidationError('Promo start date must not be greater than promo end date')


class CourseOnPromotion(models.Model):
  course = models.ForeignKey(Courses, on_delete=models.CASCADE)
  promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
  promo_price = models.DecimalField(max_digits=10, decimal_places=2,default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0.00"))])
  price_override = models.BooleanField(default=False)

  class Meta:
    unique_together = (('course', 'promotion'))


