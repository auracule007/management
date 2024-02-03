from django.urls import path, include 
from rest_framework_nested import routers 
from rest_framework_nested.routers import DefaultRouter
# from . import views


router = routers.DefaultRouter()

# router.register("cartcourses", views.CartCoursesViewSet, basename="cartcourses")
# cart_router = routers.NestedDefaultRouter(router,"cartcourses", lookup="cartcourses")
# cart_router.register("cartcoursesitem", views.CartCoursesItemViewSet, basename="cartcourses-cartcoursesitem")


urlpatterns = [
    # path("",include(router.urls)),
    # path("", include(cart_router.urls))  
]