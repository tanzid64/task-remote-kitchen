from restaurant.serializers import AddEmployeeSerializer, RestaurantListSerializer, MenuGetSerializer, MenuPostSerializer, ItemGetSerializer, ItemPostSerializer
from restaurant.models import Restaurant, Menu, Item
from restaurant.permissions import IsOwnerOrEmployeeOrReadOnly, IsResOwnerOrEmployeeOrReadOnly
from django.contrib.auth import get_user_model  
from rest_framework import generics, status, viewsets
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
            

class RestaurantViewSet(viewsets.ModelViewSet):
    """
    Any one can see the details of the restaurant.
    Only Owner or Employee can update the restaurant.
    Only Admin can delete the restaurant.
    """
    serializer_class = RestaurantListSerializer
    queryset = Restaurant.objects.all()
    permission_classes = (IsOwnerOrEmployeeOrReadOnly,)
    lookup_field = 'slug'
    http_method_names = ['get', 'put', 'patch']

class MenuViewSet(viewsets.ModelViewSet):
    """
    Restaurant slug included in URL.
    Anyone can make get request for all menus and single menu details.
    Only Owner or Employee can make post/put/patch/delete request.
    Admin users have full access.
    """
    permission_classes = [IsResOwnerOrEmployeeOrReadOnly]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MenuGetSerializer
        else:
            return MenuPostSerializer

    def get_queryset(self):
        restaurant_slug = self.kwargs.get('restaurant_slug')
        # Return an empty queryset if no slug is provided
        if not restaurant_slug:
            return Menu.objects.none()
        
        try:
            restaurant = Restaurant.objects.get(slug=restaurant_slug)
        except Restaurant.DoesNotExist:
            # Return an empty queryset if restaurant is not found
            return Menu.objects.none()

        # Filter menus by the found restaurant
        return Menu.objects.filter(restaurant=restaurant)

    def perform_create(self, serializer):
        restaurant_slug = self.kwargs.get('restaurant_slug')
        if not restaurant_slug:
            raise serializer.ValidationError("You must provide a restaurant slug.")

        try:
            restaurant = Restaurant.objects.get(slug=restaurant_slug)
        except Restaurant.DoesNotExist:
            raise serializer.ValidationError("Restaurant does not exist.")

        # Set the restaurant instance on the menu
        serializer.save(restaurant=restaurant)
    
    def perform_update(self, serializer):
        restaurant_slug = self.kwargs.get('restaurant_slug')
        if not restaurant_slug:
            raise serializer.ValidationError("You must provide a restaurant slug.")

        try:
            restaurant = Restaurant.objects.get(slug=restaurant_slug)
        except Restaurant.DoesNotExist:
            raise serializer.ValidationError("Restaurant does not exist.")

        # Set the restaurant instance on the menu
        serializer.save(restaurant=restaurant)

class ItemViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    permission_classes = [IsResOwnerOrEmployeeOrReadOnly]
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ItemGetSerializer
        else:
            return ItemPostSerializer
    def get_queryset(self):
        menu_slug = self.kwargs.get('menu_slug')
        # Return an empty queryset if no slug is provided
        if not menu_slug:
            return Item.objects.none()
        try:
            menu = Menu.objects.get(slug=menu_slug)
        except Menu.DoesNotExist:
            # Return an empty queryset if menu is not found
            return Item.objects.none()
        return Item.objects.filter(menu=menu)
    
    def perform_create(self, serializer):
        menu_slug = self.kwargs.get('menu_slug')
        if not menu_slug:
            raise serializer.ValidationError("You must provide a menu slug.")

        try:
            menu = Menu.objects.get(slug=menu_slug)
        except Menu.DoesNotExist:
            raise serializer.ValidationError("Menu does not exist.")

        # Set the menu instance on the item
        serializer.save(menu=menu)
    
    def perform_update(self, serializer):
        menu_slug = self.kwargs.get('menu_slug')
        if not menu_slug:
            raise serializer.ValidationError("You must provide a menu slug.")

        try:
            menu = Menu.objects.get(slug=menu_slug)
        except Menu.DoesNotExist:
            raise serializer.ValidationError("Menu does not exist.")

        # Set the menu instance on the item
        serializer.save(menu=menu)

# TODO: Make Order CRUD operations
# TODO: Add test cases
# TODO: API Documentation & README.md