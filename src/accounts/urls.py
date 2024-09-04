from django.urls import path
from .views import SignInView, CustomerRegistrationView, OwnerRegistrationView

urlpatterns = [
    path("signin/", SignInView.as_view(), name="signin"),
    path("customer-signup/", CustomerRegistrationView.as_view(), name="customer-signup"),
    path("owner-signup/", OwnerRegistrationView.as_view(), name="owner-signup"),
]
