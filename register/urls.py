from django.urls import path, include 
from rest_framework_nested import routers 
from rest_framework_nested.routers import DefaultRouter
from . import views


router = routers.DefaultRouter()

router.register("ordercourse", views.OrderCourseViewSet, basename="ordercourse")
# order_router = routers.NestedDefaultRouter(router,"ordercourse", lookup="ordercourse")
# order_router.register("ordercourseitem", views.OrderCourseItemViewSet, basename="ordercourse-ordercourseitem")


urlpatterns = [
    path("",include(router.urls)),
    # path("", include(order_router.urls))  
]