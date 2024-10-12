from rest_framework import permissions


class IsAdminUserWithRole(permissions.BasePermission):
    """
    Custom IsAdminUser permission that checks the roles (at least 1 must be named "Admin")
    request.user is a serialized dictionary, so we see roles as here -> "roles": ["Admin", "role2", ...]
    """
    def has_permission(self, request, view):
        if hasattr(request.user, 'roles'):  # user must have roles attribute which presents the role names list
            return "Admin" in request.user.roles
        return False


class IsAdminOrAuthenticatedAndGET(permissions.BasePermission):
    """
    Permission that allows you to reach the endpoint if one of these conditions is True:

    - you're an admin
    - you're authenticated and the HTTP method is GET
    """
    def has_permission(self, request, view):
        if request.user and request.method == "GET" or \
                hasattr(request.user, 'roles') and "Admin" in request.user.roles:
            return True
        return False


class IsAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.

    DIFFERENT FROM ORIGINAL: checks only "user isn't None"
    """

    def has_permission(self, request, view):
        return request.user is not None
