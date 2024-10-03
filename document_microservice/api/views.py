from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response

from .models import Visit
from .permissions import IsDoctorWithRole, IsDoctorOrPatientWithRole, IsAdminOrManagerWithRole
from .serializers import VisitSerializer
from .services import RoleCheckService


class VisitsByAccountView(ListAPIView):
    """
    Endpoint for retrieving a list of Visits by patient_id field

    only for doctors and the patient with given id
    """
    http_method_names = ["get"]
    allowed_methods = ["get"]
    permission_classes = [IsDoctorOrPatientWithRole,]
    serializer_class = VisitSerializer

    def get_queryset(self):
        patient_id = self.kwargs.get("id")
        response = RoleCheckService().check_role(patient_id, 'User')
        patient = response.get("user")
        if not patient:
            return Response({"details": "Couldn't find given patient"}, status=status.HTTP_404_NOT_FOUND)
        if patient['id'] != self.request.user["id"] and "Doctor" in self.request.user['roles']:
            return Response({"details": "You're not a doctor or the given patient, access denied!"},
                            status=status.HTTP_403_FORBIDDEN)
        return Visit.objects.filter(patient_id=patient_id)


class VisitByIdView(RetrieveAPIView):
    """
    Endpoint for retrieving a Visit by id field

    only for doctors and the patient linked to given Visit
    """
    http_method_names = ["get"]
    allowed_methods = ["get"]
    permission_classes = [IsDoctorOrPatientWithRole,]
    serializer_class = VisitSerializer

    def get_object(self):
        visit_id = self.kwargs.get("id")

        instance = get_object_or_404(Visit, id=visit_id)

        if instance.patient_id != self.request.user["id"] and "Doctor" in self.request.user['roles']:
            return Response({"details": "You're not a doctor or the patient linked to given object, access denied!"},
                            status=status.HTTP_403_FORBIDDEN)
        return instance

    def get_queryset(self):
        return self.get_object()


class VisitPostPutView(CreateAPIView, UpdateAPIView):
    """
    Admin/manager endpoint for creating/updating Visit objects.
    """
    http_method_names = ["post", "put"]
    allowed_methods = ["post", "put"]
    permission_classes = [IsAdminOrManagerWithRole,]
    serializer_class = VisitSerializer


# TODO: ElasticSearch
