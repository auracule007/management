from rest_framework import serializers
from . models import *
from api.models import Courses, User
from rest_framework.validators import ValidationError
from decimal import Decimal
from utils.validators import validate_id
class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = "__all__"


class CreateOrderCourseSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField()
    class Meta:
        ref_name ='CREATE_ORDER'
        model = OrderCourse
        fields = ['id','course_id','paid']
    def validate_course_id(self, value):
        return validate_id( Courses, value)
    
    
class OrderCourseSerializer(serializers.ModelSerializer):
    course = CoursesSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()
    vat = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    # user_id = serializers.IntegerField()
    class Meta:
        model= OrderCourse
        fields= [ "id","user" ,"course", "paid", "subtotal", "vat", "total"]
        read_only_fields = ['user']
    # def validate_user_id(self, value):
    #     return validate_id( User, value)
    
    def get_subtotal(self, course: OrderCourse):
        return sum([course.course.price])
    
    def get_vat(self, vat: OrderCourse):
        return vat.course.price * Decimal(0.07)
    
    def get_total(self, order_course: OrderCourse):
        subtotal = sum([order_course.course.price])
        vat = order_course.course.price * Decimal(0.07)
        total = subtotal + vat
        return total
    

# class OrderCourseItemSerializer(serializers.ModelSerializer):
#     ordercourse = OrderCourseSerializer(read_only=True)
#     class Meta:
#         model = OrderCourseItem
#         fields = ["ordercourse", "course", "date_added"]

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["user", "orderitem", "date_paid", "paid"]



    
