from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, StripeCheckOutSessionView, StripePaymentWebhookView, success_view, cancel_view
from django.urls import path, include


router = DefaultRouter()
router.register("order", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
    path('<order_id>/create-payment/', StripeCheckOutSessionView.as_view()),
    path('webhook/', StripePaymentWebhookView.as_view()),
    path('success/', success_view, name='success'),
    path('cancel/', cancel_view, name='cancel'),

]

