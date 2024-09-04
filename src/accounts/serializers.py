from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

import restaurant
from restaurant.models import Restaurant

User = get_user_model()

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password'
        )
    extra_kwargs = {
        'password': {'write_only': True}
    }
    

class OwnerRegistrationSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField()
    address = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'restaurant_name',
            'address'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Extract restaurant data
        restaurant_name = validated_data.pop('restaurant_name')
        address = validated_data.pop('address')
        
        # Set user_type
        validated_data['user_type'] = User.UserType.OWNER
        
        # Create User instance
        user = User.objects.create_user(**validated_data)
        
        # Create Restaurant instance
        Restaurant.objects.create(
            owner=user,
            restaurant_name=restaurant_name,
            address=address
        )
        
        return user
class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data["user"] = user
            else:
                raise serializers.ValidationError("Incorrect Credentials")
        else:
            raise serializers.ValidationError("Must include username and password")
        return data