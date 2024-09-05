from rest_framework.permissions import BasePermission, SAFE_METHODS

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
