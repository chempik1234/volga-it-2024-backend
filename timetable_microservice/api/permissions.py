import logging

from rest_framework import permissions

from .models import Appointment


class IsAdminOrManagerWithRole(permissions.BasePermission):
    """
    Custom IsAdminUser permission that checks the roles (at least 1 must be named "Admin" or "Manager")
    request.user is a serialized dictionary, so we see roles as here -> "roles": ["Admin", "Manager", ...]
    """
    def has_permission(self, request, view):
        if hasattr(request.user, 'roles'):  # user must have roles attribute which presents the role names list
            return "Admin" in request.user.roles or "Manager" in request.user.roles
        return False


class IsAdminOrManagerOrDoctorWithRole(permissions.BasePermission):
    """
    Custom IsAdminUser permission that checks the roles (at least 1 must be named "Admin" or "Manager" or "Doctor")
    request.user is a serialized dictionary, so we see roles as here -> "roles": ["Admin", "Manager", ...]
    """
    def has_permission(self, request, view):
        if hasattr(request.user, 'roles'):  # user must have roles attribute which presents the role names list
            return ("Admin" in request.user.roles or "Manager" in request.user.roles or
                    "Doctor" in request.user.roles)
        return False


class IsAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.

    DIFFERENT FROM ORIGINAL: checks only "user isn't None"
    """

    def has_permission(self, request, view):
        return request.user is not None


class DeleteAppointmentPermission(permissions.BasePermission):
    """
    Special permission on deleting an appointment: "only an admin/manager or the appointed user"

    (checks the appointment by id in request.kwargs
    """

    def has_permission(self, request, view):
        if request.user is not None and hasattr(request.user, "roles"):
            if "Admin" in request.user.roles or "Manager" in request.user.roles:
                return True
            obj = Appointment.objects.filter(id=request.parser_context['kwargs'].get("id"), user_id=request.user.id)
            if obj.exists():
                return True
        return False


class IsAdminOrManagerWithRoleOrGetAndAuthenticated(permissions.BasePermission):
    """
    Special permission that allows performing GET if authenticated and everything else if the user is an admin/manager
    """

    def has_permission(self, request, view):
        return (request.user is not None and
                (request.method == "GET" or "Admin" in request.user.roles or 'Manager' in request.user.roles))
