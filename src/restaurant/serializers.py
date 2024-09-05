from rest_framework import serializers
from .models import Restaurant, Item, Menu
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
class ResMiniSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Restaurant
        fields = (
            'id',
            'restaurant_name',
            'slug',
            'owner'
        )
class MenuGetSerializer(serializers.ModelSerializer):
    restaurant = ResMiniSerializer()

    class Meta:
        model = Menu
        fields = (
            'id',
            'restaurant',
            'name',
            'slug',
            'details'
        )

class MenuPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = (
            'name',
            'restaurant',
            'details'
        )
        extra_kwargs = {
            'restaurant': {'required': False}
        }

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'id',
            'menu',
            'item_name',
            'slug',
            'description',
            'price'
        )
        extra_kwargs = {
            'slug': {'read_only': True},
            'id': {'read_only': True}
        }

class MiniMenuSerializerForItem(serializers.ModelSerializer):
    restaurant_name = serializers.ReadOnlyField(source='restaurant.restaurant_name')
    restaurant_slug = serializers.ReadOnlyField(source='restaurant.slug')
    class Meta:
        model = Menu
        fields = (
            'name',
            'slug',
            'restaurant_name',
            'restaurant_slug'
        )

class ItemPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'menu',
            'item_name',
            'description',
            'price'
        )
        extra_kwargs = {
            'menu': {'required': False}
        }

class ItemGetSerializer(serializers.ModelSerializer):
    menu = MiniMenuSerializerForItem()
    class Meta:
        model = Item
        fields = (
            'id',
            'menu',
            'item_name',
            'slug',
            'description',
            'price'
        )