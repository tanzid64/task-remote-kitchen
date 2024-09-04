from rest_framework import serializers
from .models import Restaurant
from django.contrib.auth import get_user_model


User = get_user_model()

class AddEmployeeSerializer(serializers.Serializer):
    employee_id = serializers.UUIDField()
    restaurant_id = serializers.UUIDField()

class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
