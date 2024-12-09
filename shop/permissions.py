from rest_framework.permissions import BasePermission

class IsStaffForPost(BasePermission):
    """
    Permission: only for staff users can POST data.
    """

    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH'] and not request.user.is_staff:
            return False
        return True
