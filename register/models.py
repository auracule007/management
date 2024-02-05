from django.db import models
from api.models import *
# Create your models here.


class OrderCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    day_enrolled = models.DateTimeField(auto_now_add=True)
    is_enrolled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name}"
    
class OrderCourseItem(models.Model):
    ordercourse = models.ForeignKey(OrderCourse, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ordercourse
    
class Payment(models.Model):
    user =  models.ForeignKey(User, on_delete=models.PROTECT)
    orderitem = models.ForeignKey(OrderCourseItem, on_delete=models.PROTECT)
    amount = models.IntegerField()
    date_paid = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username 






































































# class OrderCourse(models.Model):
#     courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
#     cartcoursesitem = models.ManyToManyField(CartCoursesItem)
#     price = models.IntegerField()
#     date_added = models.DateTimeField(auto_now_add=True)
#     amount = models.IntegerField()
#     paid = models.BooleanField(default=False)


# class OrderItem(models.Model):
#     ordercourse = models.ForeignKey(OrderCourse, on_delete=models.CASCADE)
#     date_created = models.DateTimeField(auto_now_add=True)

# class Payment(models.Model):
#     user =  models.ForeignKey(User, on_delete=models.PROTECT)
#     orderitem = models.ForeignKey(OrderItem, on_delete=models.PROTECT)
#     course = models.ForeignKey(Courses, on_delete=models.PROTECT)
#     amount = models.IntegerField()
#     date_paid = models.DateTimeField(auto_now_add=True)
#     paid = models.BooleanField(default=False)