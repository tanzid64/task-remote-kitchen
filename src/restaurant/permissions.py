from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth import get_user_model
from restaurant.models import Restaurant

User = get_user_model()

class IsOwnerOrEmployeeOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners or employees to update or delete
    a restaurant.
    Admin users have full access.
    """
    
    def has_object_permission(self, request, view, obj):
        # Allow read-only access to any user
        if request.method in SAFE_METHODS:
            return True
        
        # Allow all access to admins
        if request.user.is_staff:
            return True
        
        # Allow owners and employees to update (PUT/PATCH) a restaurant
        if request.method in ['PUT', 'PATCH']:
            return request.user == obj.owner or request.user in obj.employees.all()
        
        # Allow owners to delete a restaurant
        if request.method == 'DELETE':
            return request.user == obj.owner
        
        return False
    

class IsResOwnerOrEmployeeOrReadOnly(BasePermission):
    """
    Anyone can make get request.
    Only Owner or Employee can make post/put/patch/delete request.
    Admin users have full access.
    """

    def has_permission(self, request, view,):
        # Allow read-only access to any user
        if request.method in SAFE_METHODS:
            return True
        
        # Check if user is authenticated and is either owner or employee
        # if not request.user.is_authenticated or not (request.user.user_type == User.UserType.OWNER or request.user.user_type == User.UserType.EMPLOYEE):
        #     return False
        
        # Allow all access to admins
        if request.user.is_staff:
            return True
        
        # For POST, PUT, PATCH, DELETE requests, check if user is owner or employee
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            # Extract restaurant id from request data or URL
            restaurant_slug = view.kwargs.get('restaurant_slug')
            if not restaurant_slug:
                return False
            try:
                restaurant = Restaurant.objects.get(slug=restaurant_slug)
            except Restaurant.DoesNotExist:
                return False
            
            return (request.user == restaurant.owner or 
                request.user in restaurant.employees.all())
        
        return False
        
