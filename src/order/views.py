import stripe
import json
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, Payment
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import viewsets


User = get_user_model()


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return Order.objects.filter(placed_by=self.request.user)
    def perform_create(self, serializer):
        serializer.save(placed_by=self.request.user)



class StripeCheckOutSessionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs) -> Response:
        # Get order id from url
        order_id = self.kwargs.get('order_id')

        # Get order from Order model by order id
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({
                'error': 'Order does not exist'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if order belongs to user
        if order.placed_by != self.request.user:
            return Response({
                'error': 'Order does not belong to you'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if order payment status is not paid
        if order.payment_status == Order.PaymentStatus.PAID:
            return Response({
                "order_id": order_id,
                'payment_status': order.payment_status,
                'payment_intent_id': order.payments.last().stripe_payment_intent_id
            }, status=status.HTTP_200_OK)
        
        # Check if order payment method is not card
        if order.payment_method != Order.PaymentMethod.CARD:
            return Response({
                'error': 'Order payment method is not card'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate order amount
        order_amount = int(order.total * 100) # converting usd to cents

        # Set stripe secret key
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f"order_id: {order_id}",
                        },
                        'unit_amount': order_amount
                    },
                    'quantity': 1
                }],
                mode='payment',
                success_url=settings.STRIPE_SUCCESS_URL,
                cancel_url=settings.STRIPE_CANCEL_URL
            )

            # Create a Payment model
            Payment.objects.create(
                order=order,
                checkout_session_id=checkout_session.id,
                amount = order.total
            )

            return Response({
                "order_id": order_id,
                'checkout_url': checkout_session.url
            }, status=status.HTTP_200_OK)
        
        except stripe.error.CardError as e:
            return Response({
                'message': "Card Payment Failed",
                'error': str(e.user_message)
            }, status=status.HTTP_400_BAD_REQUEST)
        
class StripePaymentWebhookView(APIView):
    """
    Stripe webhook view to handle checkout session completed event.
    """
    def post(self, request, *args, **kwargs) -> Response:
        payload = request.body
        event = None
        try:
            event_json = json.loads(payload.decode('utf-8'))
            event = stripe.Event.construct_from(
                event_json, settings.STRIPE_SECRET_KEY, settings.STRIPE_WEBHOOK_SECRET_KEY
            )
        except ValueError as e:
            #Invalid Payload
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle the events
        if event.type == 'checkout.session.completed':
            try:
                # Get Chekout session object
                checkout_session_obj = event.data.object

                # Collect data from checkout session object
                checkout_id = checkout_session_obj.id
                amount = checkout_session_obj.amount_total/100 # converting cents to usd
                payer_email = checkout_session_obj.customer_details.email
                payer_name = checkout_session_obj.customer_details.name
                payer_phone = checkout_session_obj.customer_details.phone
                stripe_payment_intent_id = checkout_session_obj.payment_intent
                payment_status = checkout_session_obj.payment_status
                if payment_status == 'paid':
                    # update payment model's data
                    payment_obj = Payment.objects.get(checkout_session_id=checkout_id)
                    payment_obj.stripe_payment_intent_id = stripe_payment_intent_id
                    payment_obj.payer_email = payer_email
                    payment_obj.payer_name = payer_name
                    payment_obj.payer_phone = payer_phone
                    payment_obj.payment_status = Payment.PaymentStatus.PAID
                    payment_obj.amount = float(amount)
                    payment_obj.save()

                    # update order model's data
                    order_obj = Order.objects.get(id=payment_obj.order.id)
                    order_obj.payment_status = Order.PaymentStatus.PAID
                    order_obj.payment_id = payment_obj.id
                    order_obj.save()
            except Payment.DoesNotExist:
                return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
            except Order.DoesNotExist:
                return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            # Unhandled event type
            return Response({"error": "Unhandled event type"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'success': True
        }, status=status.HTTP_200_OK)


from django.http import HttpResponse
def success_view(request):
    return HttpResponse('Payment is successfully processed.')

def cancel_view(request):
    return HttpResponse('Payment is cancelled.')