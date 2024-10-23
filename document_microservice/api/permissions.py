import logging

from django.shortcuts import get_object_or_404
from rest_framework import permissions

from .grpc_consume_produce import grpc_check_user_and_role
from .models import Visit


class IsAdminOrManagerOrDoctorWithRole(permissions.BasePermission):
    """
    Custom IsAdminUser permission that checks the roles (at least 1 must be named "Admin" or "Manager" or "Doctor")
    request.user is a serialized dictionary, so we see roles as here -> "roles": ["Admin", "Manager", ...]
    """
    def has_permission(self, request, view):
        if hasattr(request.user, 'roles'):  # user must have roles attribute which presents the role names list
            return ("Admin" in request.user.roles or "Manager" in request.user.roles or
                    'Doctor' in request.user.roles)
        return False


class IsAdminOrManagerWithRole(permissions.BasePermission):
    """
    Custom IsAdminUser permission that checks the roles (at least 1 must be named "Admin" or "Manager")
    request.user is a serialized dictionary, so we see roles as here -> "roles": ["Admin", "Manager", ...]
    """
    def has_permission(self, request, view):
        if hasattr(request.user, 'roles'):  # user must have roles attribute which presents the role names list
            return "Admin" in request.user.roles or "Manager" in request.user.roles
        return False


class IsDoctorWithRole(permissions.BasePermission):
    """
    Custom IsAdminUser permission that checks the roles (at least 1 must be named "Doctor")
    request.user is a serialized dictionary, so we see roles as here -> "roles": ["Doctor", ...]

    - Even pure admins can't pass this permission !!!!!
    """
    def has_permission(self, request, view):
        if hasattr(request.user, 'roles'):  # user must have roles attribute which presents the role names list
            return "Doctor" in request.user.roles
        return False


class IsDoctorOrPatientWithRole(permissions.BasePermission):
    """
    Custom IsAdminUser permission that checks the roles (at least 1 must be named "Doctor" or "User")
    request.user is a serialized dictionary, so we see roles as here -> "roles": ["Doctor", ...]

    - Even pure admins can't pass this permission !!!!!
    """
    def has_permission(self, request, view):
        if hasattr(request.user, 'roles'):  # user must have roles attribute which presents the role names list
            return "Doctor" in request.user.roles or 'User' in request.user.roles
        return False


class IsDoctorOrLinkedPatientToVisit(permissions.BasePermission):
    """
    Permission for accessing Visits that allows it if the user is a doctor or the patient linked to given Visit
    """

    def has_permission(self, request, view):
        if request.user is None:
            return False
        visit_id = request.parser_context['kwargs'].get("id")
        instance = Visit.objects.filter(id=visit_id)
        if instance.exists():
            instance = instance.first()
            return instance.patient_id == request.user.id or "Doctor" in request.user.roles
        return False


class IsDoctorOrGivenPatient(permissions.BasePermission):
    """
    Permission for viewing history by patient id. Allows if the user is a doctor or the given patient
    """

    def has_permission(self, request, view):
        patient_id = request.parser_context['kwargs'].get("id")
        patient, is_valid = grpc_check_user_and_role(patient_id, 'User')
        if not is_valid:
            return False
        if patient.id == request.user.id or "Doctor" in request.user.roles:
            return True


class GetPutVisitByIdPermission(permissions.BasePermission):
    """
    Special permission: if GET then IsDoctorOrLinkedPatientToVisit, else IsAdminOrManagerWithRole
    """

    def has_permission(self, request, view):
        logging.error(f"KFDSA JDFLKSAJ DK {request.method} {request.method == "PUT"} {IsDoctorOrLinkedPatientToVisit().has_permission(request, view)} {IsAdminOrManagerWithRole().has_permission(request, view)}")
        if request.method == "GET":
            return IsDoctorOrLinkedPatientToVisit().has_permission(request, view)
        else:
            return IsAdminOrManagerWithRole().has_permission(request, view)
