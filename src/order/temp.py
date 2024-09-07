try:
                card_details= {
                    
                        "number": data_dict['card_number'],
                        "exp_month": data_dict['expiry_month'],
                        "exp_year": data_dict['expiry_year'],
                        "cvc": data_dict['cvc'],
                    
                }
            
                payment_intent = stripe.PaymentIntent.create(
                    amount=order_amount,
                    currency='usd',
                )
                payment_intent_modified = stripe.PaymentIntent.modify(
                    payment_intent.id,
                    payment_method=(
                        number=data_dict['card_number'],
                        exp_month=data_dict['expiry_month'],
                        exp_year=data_dict['expiry_year'],
                        cvc=data_dict['cvc'],
                    ),
                )

                try:
                    payment_confirm = stripe.PaymentIntent.confirm(
                        payment_intent['id'],
                    )
                    payment_intent_modified = stripe.PaymentIntent.retrieve(
                        payment_intent['id']
                    )
                except:
                    payment_intent_modified = stripe.PaymentIntent.retrieve(payment_intent['id'])
                    payment_confirm = {
                        "stripe_payment_error": "Failed",
                        "code": payment_intent_modified['last_payment_error']['code'],
                        "message": payment_intent_modified['last_payment_error']['message'],
                        'status': "Failed"
                    }
                
                if payment_intent_modified and payment_intent_modified.status == 'succeeded':
                    order.payment_status = Order.PaymentStatus.PAID
                    order.payment_id = payment_intent.id
                    order.save()
                    payment = Payment.objects.create(
                        order=order,
                        payment_status=Payment.PaymentStatus.PAID,
                    )
                    payment.save()
                    return Response({
                        'message': "Card Payment Success",
                        "card_details": card_details,
                        "payment_intent": payment_intent_modified,
                        "payment_confirm": payment_confirm
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'message': "Card Payment Failed",
                        "card_details": card_details,
                        "payment_intent": payment_intent_modified,
                        "payment_confirm": payment_confirm
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            except stripe.error.CardError as e:
                return Response({
                    'message': "Card Payment Failed",
                    'error': str(e.user_message)
                }, status=status.HTTP_400_BAD_REQUEST)
            
            except stripe.error.StripeError as e:
                return Response({
                    'message': "Card Payment Failed",
                    'error': str(e.user_message)
                }, status=status.HTTP_400_BAD_REQUEST)