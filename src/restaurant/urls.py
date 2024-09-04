from django.urls import path
from .views import AddEmployeeView, RestaurantListView, RestaurantDetailView

urlpatterns = [
    path("add-employee/", AddEmployeeView.as_view(), name="add-employee"),
    path("all/", RestaurantListView.as_view(), name="all-restaurant-list"),
    path("<str:slug>/", RestaurantDetailView.as_view(), name="restaurant-detail"),
]
