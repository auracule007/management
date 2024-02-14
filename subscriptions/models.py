from django.db import models
from api.models import User
from utils.choices import PLAN_CHIOCES,PLAN_NAME
import datetime

from utils.dates import calculate_expiration_date

class Plan(models.Model):
    name = models.CharField(max_length=255,choices=PLAN_NAME)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    interval = models.CharField(max_length=20, help_text='weekly, monthly, yearly', choices=PLAN_CHIOCES, default='Free')  
    features = models.TextField(help_text='Plan benefits')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    pending_status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    start_date = models.DateTimeField(default=datetime.datetime.now)
    expiration_date = models.DateTimeField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.plan.name}'
    
    def save(self, *args, **kwargs):
      if not self.expiration_date:
        self.expiration_date = calculate_expiration_date(self.start_date, self.plan.interval)
      super(Subscription, self).save(*args, **kwargs)
