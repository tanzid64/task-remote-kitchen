from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only requests for any user
        if request.method in SAFE_METHODS:
            return True
        
        # Allow full access to the owners
        return obj.owner == request.user

class IsEmployeeOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only requests for any user
        if request.method in SAFE_METHODS:
            return True
        
        # Allow full access to the employees
        return request.user in obj.employees.all()
    
class OwnerOrEmployeeOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user in obj.employees.all()