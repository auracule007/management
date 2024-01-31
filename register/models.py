from django.db import models
from api.models import *
# Create your models here.

class CartCourses(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    course = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    paid = models.BooleanField(default=False)
    day_enrolled = models.DateTimeField(auto_now_add=True)
    is_enrolled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} -- {self.course.name}"
    
class CartCoursesItem(models.Model):
    cartcourses = models.ForeignKey(CartCourses, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shopcart.name
    
class OrderCourse(models.Models):
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
    cartcoursesitem = models.ManyToManyField(CartCoursesItem)
    price = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    ordercourse = models.ForeignKey(OrderCourse, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)