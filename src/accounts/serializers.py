from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    