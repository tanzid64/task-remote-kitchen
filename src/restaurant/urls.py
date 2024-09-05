from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AddEmployeeView, RestaurantViewSet

router = DefaultRouter()
router.register("", RestaurantViewSet)

urlpatterns = [
    path("add-employee/", AddEmployeeView.as_view(), name="add-employee"),
    path("", include(router.urls)),
]
