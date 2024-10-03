from rest_framework import permissions


class IsAdminOrManagerOrDoctorWithRole(permissions.BasePermission):
    """
    Custom IsAdminUser permission that checks the roles (at least 1 must be named "Admin" or "Manager" or "Doctor")
    request.user is a serialized dictionary, so we see roles as here -> "roles": ["Admin", "Manager", ...]
    """
    def has_permission(self, request, view):
        if hasattr(request.user, 'roles'):  # user must have roles attribute which presents the role names list
            return ("Admin" in request.user["roles"] or "Manager" in request.user['roles'] or
                    'Doctor' in request.user['roles'])
        return False


class IsAdminOrManagerWithRole(permissions.BasePermission):
    """
    Custom IsAdminUser permission that checks the roles (at least 1 must be named "Admin" or "Manager")
    request.user is a serialized dictionary, so we see roles as here -> "roles": ["Admin", "Manager", ...]
    """
    def has_permission(self, request, view):
        if hasattr(request.user, 'roles'):  # user must have roles attribute which presents the role names list
            return "Admin" in request.user["roles"] or "Manager" in request.user['roles']
        return False


class IsDoctorWithRole(permissions.BasePermission):
    """
    Custom IsAdminUser permission that checks the roles (at least 1 must be named "Doctor")
    request.user is a serialized dictionary, so we see roles as here -> "roles": ["Doctor", ...]

    - Even pure admins can't pass this permission !!!!!
    """
    def has_permission(self, request, view):
        if hasattr(request.user, 'roles'):  # user must have roles attribute which presents the role names list
            return "Doctor" in request.user['roles']
        return False


class IsDoctorOrPatientWithRole(permissions.BasePermission):
    """
    Custom IsAdminUser permission that checks the roles (at least 1 must be named "Doctor" or "User")
    request.user is a serialized dictionary, so we see roles as here -> "roles": ["Doctor", ...]

    - Even pure admins can't pass this permission !!!!!
    """
    def has_permission(self, request, view):
        if hasattr(request.user, 'roles'):  # user must have roles attribute which presents the role names list
            return "Doctor" in request.user['roles'] or 'User' in request.user['roles']
        return False
