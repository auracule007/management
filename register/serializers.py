from rest_framework import serializers
from . models import *
from api.models import Courses
from rest_framework.validators import ValidationError

    
class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = "__all__"
        
class CartCoursesItemSerializers(serializers.ModelSerializer):
    course = CoursesSerializer()
    class Meta:
        model = CartCoursesItem
        fields = ["cartcourses", "course", "date_added"]

class CartCoursesSerializer(serializers.ModelSerializer):
    cartcourses = serializers.SerializerMethodField()
    class Meta:
        model = CartCourses
        fields = ["user", "cartcourses"]    

    def get_cartcourses(self, obj: CartCoursesItem):
        return obj.cartcoursesitem_set.values("course", "date_added")

    def validate_course_id(self, value):
        if not Courses.objects.filter(course_id=value).exists():
            raise serializers.ValidationError("The course you are trying to add is not available")
        return value
     


    
