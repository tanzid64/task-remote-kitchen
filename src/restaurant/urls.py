from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AddEmployeeView, RestaurantViewSet, MenuViewSet

router = DefaultRouter()
router.register("restaurant", RestaurantViewSet, basename="restaurant")
router.register(r'(?P<restaurant_slug>[\w-]+)/menu', MenuViewSet, basename='menu')

urlpatterns = [
    path("add-employee/", AddEmployeeView.as_view(), name="add-employee"),
    path("", include(router.urls)),
]
