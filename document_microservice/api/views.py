from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response

from .grpc_consume_produce import grpc_check_user_and_role
from .models import Visit
from .permissions import IsDoctorOrLinkedPatientToVisit, IsDoctorOrPatientWithRole, IsAdminOrManagerWithRole, \
    IsDoctorOrGivenPatient, GetPutVisitByIdPermission
from .serializers import VisitSerializer


class VisitsByAccountView(ListAPIView):
    """
    Endpoint for retrieving a list of Visits by patient_id field

    only for doctors and the patient with given id
    """
    http_method_names = ["get"]
    allowed_methods = ["get"]
    permission_classes = [IsDoctorOrGivenPatient,]
    serializer_class = VisitSerializer

    def get_queryset(self):
        patient_id = self.kwargs.get("id")
        return Visit.objects.filter(patient_id=patient_id)


@extend_schema_view(
    get=extend_schema(
        description="Endpoint for retrieving a Visit by id field\nonly "
                    "for doctors and the patient linked to given Visit"
    ),
    put=extend_schema(
        description="Admin/manager endpoint for creating Visit objects."
    )
)
class GetPutVisitByIdView(RetrieveAPIView, UpdateAPIView):
    """
    Endpoint for retrieving a Visit by id field

    only for doctors and the patient linked to given Visit
    """
    http_method_names = ["get", 'put']
    allowed_methods = ["get", 'put']
    permission_classes = [GetPutVisitByIdPermission,]
    serializer_class = VisitSerializer
    lookup_field = "id"

    def get_object(self):
        visit_id = self.kwargs.get("id")
        instance = get_object_or_404(Visit, id=visit_id)
        return instance

    def get_queryset(self):
        return self.get_object()


class VisitCreateView(CreateAPIView):
    """
    Admin/manager endpoint for creating Visit objects.
    """
    http_method_names = ["post"]
    allowed_methods = ["post"]
    permission_classes = [IsAdminOrManagerWithRole,]
    serializer_class = VisitSerializer

