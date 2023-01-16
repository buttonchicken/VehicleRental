from rest_framework.permissions import BasePermission,SAFE_METHODS

class isadmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_superuser