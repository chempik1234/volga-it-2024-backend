from rest_framework import permissions


class IsAdminUserWithRole(permissions.BasePermission):
    """
    Custom IsAdminUser permission that checks the roles (at least 1 must be named "Admin")
    request.user is a serialized dictionary, so we see roles as here -> "roles": ["Admin", "role2", ...]
    """
    def has_permission(self, request, view):
        if hasattr(request.user, 'roles'):  # user must have roles attribute which presents the role names list
            return "Admin" in request.user["roles"]
        return False
