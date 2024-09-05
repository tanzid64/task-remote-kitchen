from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AddEmployeeView, RestaurantViewSet, MenuViewSet, ItemViewSet

router = DefaultRouter()
router.register("restaurant", RestaurantViewSet, basename="restaurant")
router.register(r'(?P<restaurant_slug>[\w-]+)/menu', MenuViewSet, basename='menu')
router.register(r'(?P<restaurant_slug>[\w-]+)/(?P<menu_slug>[\w-]+)/item', ItemViewSet, basename='item')

urlpatterns = [
    path("", include(router.urls)),
    path("add-employee/", AddEmployeeView.as_view(), name="add-employee"),
]
