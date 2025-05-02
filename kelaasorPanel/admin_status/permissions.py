from rest_framework.permissions import BasePermission

class IsSuperUserType(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True
        return False

