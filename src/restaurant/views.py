from django.shortcuts import render
from restaurant.serializers import AddEmployeeSerializer, RestaurantListSerializer
from restaurant.models import Restaurant
from restaurant.permissions import IsOwnerOrReadOnly, IsEmployeeOrReadOnly
from django.contrib.auth import get_user_model  
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.

User = get_user_model()

class AddEmployeeView(APIView):
    """
    Only Owner can add Employee.
    User with CUSTOMER user type only can be converted as EMPLOYEE.
    """
    def post(self, request, *args, **kwargs):
        serializer = AddEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee_id = serializer.validated_data['employee_id']
            restaurant_id = serializer.validated_data['restaurant_id']
            # Find Restaurant
            try:
                restaurant = Restaurant.objects.get(id=restaurant_id)
            except Restaurant.DoesNotExist:
                return Response({"error": "Restaurant does not exist"}, status=status.HTTP_404_NOT_FOUND)
            # Find Employee
            try:
                employee = User.objects.get(id=employee_id)
            except User.DoesNotExist:
                return Response({"error": "Employee does not exist"}, status=status.HTTP_404_NOT_FOUND)
            # Only Owner can add Employee
            if request.user != restaurant.owner:
                return Response({"error": "Only Owner can add Employee"}, status=status.HTTP_403_FORBIDDEN)
            # Check if Employee is already added to the restaurant
            if employee.user_type == User.UserType.OWNER or employee.user_type == User.UserType.EMPLOYEE:
                return Response({"error": "You cannot add other restaurant's Employee."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if Employee is already added to another restaurant
            if User.objects.filter(restaurant=restaurant, id=employee_id).exists():
                return Response({"error": "Employee is already added to another restaurant."}, status=status.HTTP_400_BAD_REQUEST)

            # Add Employee
            restaurant.employees.add(employee)
            # Update user type to employee
            employee.user_type = User.UserType.EMPLOYEE
            employee.save()
            return Response({"message": "Employee added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

class RestaurantListView(generics.ListAPIView):
    serializer_class = RestaurantListSerializer
    def get_queryset(self):
        return Restaurant.objects.all()

class RestaurantDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = RestaurantListSerializer
    lookup_field = 'slug'
    pagination_class = (IsOwnerOrReadOnly, IsEmployeeOrReadOnly)
    def get_queryset(self):
        return Restaurant.objects.all()
    
# TODO: Test Update and Delete methods
# TODO: Make Item & Menu CRUD operations
# TODO: Make Order CRUD operations
# TODO: Add test cases
# TODO: API Documentation & README.md