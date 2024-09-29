from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


class IsAdminUserWithRole(permissions.BasePermission):
    """
    Custom IsAdminUser permission that checks the roles (at least 1 must be named "Admin"
    """
    def has_permission(self, request, view):
        if hasattr(request.user, 'roles'):  # user must have roles attribute which describes the M2M with Role model
            return request.user.roles.filter(name="Admin").exists()  # if user != None we can find the Admin one
        return False


class IsAdminOrAuthenticatedAndGET(permissions.BasePermission):
    """
    Permission that allows GET for authenticated users and makes every other method admin-only
    """
    def has_permission(self, request, view):
        return (IsAuthenticated().has_permission(request, view) and request.method == "GET" or
                IsAdminUserWithRole().has_permission(request, view))
