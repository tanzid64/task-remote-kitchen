import stripe
from django.conf import settings
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, Payment
from restaurant.models import Item, Restaurant
from .serializers import OrderSerializer, CardInformationSerializer
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


    serializer_class = CardInformationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data_dict = serializer.validated_data
            order_id = self.kwargs.get('order_id')
            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                return Response({'error': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
            if order.placed_by != self.request.user:
                return Response({'error': 'Order does not belong to you'}, status=status.HTTP_400_BAD_REQUEST)
            
            if order.payment_status == Order.PaymentStatus.PAID:
                return Response({'error': 'Order is already paid'}, status=status.HTTP_400_BAD_REQUEST)
            
            if order.payment_method != Order.PaymentMethod.CARD:
                return Response({'error': 'Order payment method is not card'}, status=status.HTTP_400_BAD_REQUEST)
            
            order_amount = int(order.total * 100)
            
            stripe.api_key = settings.STRIPE_SECRET_KEY
            
            try:
                # card details from validate serializer
                card_details = {
                    "number": data_dict['number'],
                    "exp_month": data_dict['exp_month'],
                    "exp_year": data_dict['exp_year'],
                    "cvc": data_dict['cvc'],
                }
                # Create payment method with card information
                payment_method = stripe.PaymentMethod.create(
                    type="card",
                    card=card_details,
                )

                updated_payment_method = stripe.PaymentMethod.retrieve(payment_method['id'])
                print(updated_payment_method)
                payment_intent = stripe.PaymentIntent.create(
                    amount=order_amount,
                    currency='usd',
                )
                try:
                    confirm_payment_intent = stripe.PaymentIntent.confirm(
                    payment_intent['id'],
                    payment_method=updated_payment_method['id'],
                )
                except:
                    payment_intent = stripe.PaymentIntent.retrieve(payment_intent['id'])
                    return Response({
                        'message': "Card Payment Failed",
                        "card_details": card_details,
                        "payment_intent": payment_intent
                    })
                if confirm_payment_intent['status'] == 'succeeded':
                    return Response({
                    "message": "Card Payment Success",
                    "card_details": card_details,
                    "payment_intent": payment_intent,
                    "payment_confirm": confirm_payment_intent
                }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'message': "Card Payment Failed",
                        "card_details": card_details,
                        "payment_intent": payment_intent,
                        "payment_confirm": confirm_payment_intent
                    }, status=status.HTTP_400_BAD_REQUEST)
            except:
                pass
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    permission_classes = [IsAuthenticated]
    serializer_class = CardInformationSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Get validate data from serializer/request
            data = serializer.validated_data

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
                    'error': 'Order is already paid'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if order payment method is not card
            if order.payment_method != Order.PaymentMethod.CARD:
                return Response({
                    'error': 'Order payment method is not card'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Calculate order amount
            order_amount = int(order.total * 100) # converting usd to cents

            # Set stripe secret key
            stripe.api_key = settings.STRIPE_SECRET_KEY

            # create a fake payment method for development, in production we will get payment method id from client side
            card_info = {
                "number": data['card_number'],
                "exp_month": data['expiry_month'],
                "exp_year": data['expiry_year'],
                "cvc": data['cvc'],
            }

            try:
                payment_method = stripe.PaymentMethod.create(
                    type="card",
                    card=card_info
                )
                return Response({
                    "message": "Card Payment Success",
                    "card_details": card_info,
                    "payment_method": payment_method
                })
            except stripe.error.CardError as e:
                return Response({
                    'message': "Card Payment Failed",
                    'error': str(e.user_message)
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
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
    def post(self, request, *args, **kwargs):
        event = None
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        webhook_secret = settings.STRIPE_WEBHOOK_SECRET_KEY

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError as e:
            # Invalid payload
            return Response({"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
            # Handle successful payment intent
            pass

        elif event['type'] == 'payment_method.attached':
            # Handle attached payment method
            pass

        elif event['type'] == 'checkout.session.completed':
            checkout_session_obj = event['data']['object']

            try:
                print("okay")
                checkout_id = checkout_session_obj['id']
                amount = checkout_session_obj['amount_total'] / 100
                payer_email = checkout_session_obj['customer_details'].get('email')
                payer_name = checkout_session_obj['customer_details'].get('name')
                payer_phone = checkout_session_obj['customer_details'].get('phone')
                stripe_payment_intent_id = checkout_session_obj['payment_intent']
                payment_status = checkout_session_obj['payment_status']

                # Update Payment model
                payment_obj = Payment.objects.get(checkout_session_id=checkout_id)
                payment_obj.payer_email = payer_email
                payment_obj.payer_name = payer_name
                payment_obj.payer_phone = payer_phone
                payment_obj.stripe_payment_intent_id = stripe_payment_intent_id
                payment_obj.payment_status = payment_status
                payment_obj.amount = float(amount)
                payment_obj.save()

                # Update Order model
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