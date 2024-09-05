from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import SignInSerializer, CustomerRegistrationSerializer, OwnerRegistrationSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from restaurant.models import Restaurant
from rest_framework.response import Response
from rest_framework import status, generics
# Create your views here.
User = get_user_model()

class CustomerRegistrationView(generics.CreateAPIView):
    """
    Register a new user, and sign in automatically.
    New user will be customer type as we set default type as customer in the model field.
    """
    serializer_class = CustomerRegistrationSerializer
    queryset = User.objects.all()
    def create(self, request, *args, **kwargs) -> Response:
        # Using the serializer to validate and create the customer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Create a token for the newly created user
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user_id": user.pk,
            "user_type": user.user_type,
            "username": user.username
        }, status=status.HTTP_201_CREATED)
    
class OwnerRegistrationView(generics.CreateAPIView):
    serializer_class = OwnerRegistrationSerializer

    def post(self, request, *args, **kwargs):
        # Serialize and create user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token for the newly created user
        token, created = Token.objects.get_or_create(user=user)

        restaurant = Restaurant.objects.get(owner=user)
        
        return Response({
            "token": token.key,
            "user_id": user.pk,
            "user_type": user.user_type,
            "username": user.username,
            "restaurant_name": restaurant.restaurant_name,
            "address": restaurant.address
        }, status=status.HTTP_201_CREATED)
    
class SignInView(APIView):
    """
    Sign in a user with username and password.
    """
    def post(self, request, *args, **kwargs) -> Response:
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.pk,
                "user_type": user.user_type,
                "username": user.username
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
