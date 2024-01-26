from django.db import models
from api.models import User
from utils.choices import *


class UserPerformance(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  progress_percentage = models.DecimalField(max_digits=5, decimal_places=2)
  completion_status = models.CharField(max_length=50, default='Uncomplete', choices=COMPLETION_STATUS)

  def __str__(self):
    return f'{self.user.username} -{self.progress_percentage}'