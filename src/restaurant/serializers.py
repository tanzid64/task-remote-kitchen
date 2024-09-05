from rest_framework import serializers
from .models import Restaurant
from django.contrib.auth import get_user_model


User = get_user_model()

class AddEmployeeSerializer(serializers.Serializer):
    employee_id = serializers.UUIDField()
    restaurant_id = serializers.UUIDField()


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'username'
        )
class RestaurantListSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    employees = OwnerSerializer(many=True)
    class Meta:
        model = Restaurant
        fields = (
            'id',
            'restaurant_name',
            'slug',
            'address',
            'owner',
            'employees'
        )
        extra_kwargs = {
            'slug': {'read_only': True}
        }
