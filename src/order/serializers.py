from rest_framework import serializers
from restaurant.models import Item
from .models import Order, OrderItem, Payment
from .utils import (check_expiry_month, check_expiry_year, check_cvc)

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ['id', 'placed_by', 'payment_status', 'payment_method', 'payment_id', 'order_items', 'subtotal', 'total']
        extra_kwargs = {
            'placed_by': {'required': False},
        }
    read_only_fields = ['id', 'subtotal', 'total', 'payment_status', 'payment_id']

    def create(self, validated_data):
        # Extract order_items data from validated_data
        order_items_data = validated_data.pop('order_items')
        
        # Create the Order instance
        order = Order.objects.create(**validated_data)
        
        # Create OrderItem instances
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order
    
# Card Serializer
"""
Will collect the card informations from frontend and make a payment request on stripe.
"""
class CardInformationSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=150, required=True)
    expiry_month = serializers.CharField(max_length=2, required=True, validators=[check_expiry_month])
    expiry_year = serializers.CharField(max_length=4, required=True, validators=[check_expiry_year])
    cvc = serializers.CharField(max_length=3, required=True, validators=[check_cvc])