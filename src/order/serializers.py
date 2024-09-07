from rest_framework import serializers
from .models import Order, OrderItem

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