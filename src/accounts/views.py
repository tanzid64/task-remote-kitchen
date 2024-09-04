from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import SignInSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
User = get_user_model()

class SignInView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.pk,
                "user_type": user.user_type,
                "username": user.username
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)