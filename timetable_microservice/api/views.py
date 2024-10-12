import json
from datetime import datetime, timedelta

from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, inline_serializer
from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView, ListAPIView, \
    GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Appointment, Timetable
from .permissions import IsAdminOrManagerWithRole, IsAuthenticated, DeleteAppointmentPermission, \
    IsAdminOrManagerWithRoleOrGetAndAuthenticated
from .serializers import TimetableSerializer, AppointmentSerializer


class CreateTimetableView(CreateAPIView):
    """
    Simple timetable creation view

    POST /api/Timetable
    """
    permission_classes = [IsAdminOrManagerWithRole,]
    serializer_class = TimetableSerializer
    http_method_names = ["post"]
    allowed_methods = ["post"]


@extend_schema_view(
    put=extend_schema(
        description="Change timetable by id\nPUT /api/Timetable/{id}\nOnly admins and managers\nCan't perform if"
                    "there are appointments for given object!"
    ),
    delete=extend_schema(
        description="Delete timetable by id\nPUT /api/Timetable/{id}\nOnly admins and managers"
    )
)
class TimetablePutDeleteViewSet(DestroyAPIView, UpdateAPIView):
    """
    Simple timetable PUT and DELETE endpoint
    PUT DELETE /api/Timetable/{id}
    """
    permission_classes = [IsAdminOrManagerWithRole,]
    serializer_class = TimetableSerializer
    http_method_names = ["put", "delete"]
    allowed_methods = ["put", "delete"]
    queryset = Timetable.objects.all()
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if Appointment.objects.filter(timetable=instance).exists():
            return Response({"detail": "A timetable that someone has appointed to can't be changed.."},
                            status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, *kwargs)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter("from", description="From (timetable is active at this moment of time or "
                                                 "starts after this and before 'from')",
                             location=OpenApiParameter.QUERY,
                             default="1970-01-01T00:00:00Z"),
            OpenApiParameter("to", description="To (timetable is active at this moment of time or "
                                               "ends between 'from' and 'to')",
                             location=OpenApiParameter.QUERY,
                             default="9999-12-31T23:59:59Z")
        ]
    )
)
class GetDeleteTimeTablesByHospitalInPeriodView(ListAPIView, DestroyAPIView):
    """
    - Endpoint to retrieve list of all timetables for given hospital in given period

    GET /api/Timetable/Hospital/{id} ?from=<>&to=<>

    - Endpoint for deleting all timetables by hospital_id

    DELETE /api/Timetable/Hospital/{id}
    """
    permission_classes = [IsAdminOrManagerWithRoleOrGetAndAuthenticated,]
    serializer_class = TimetableSerializer
    lookup_field = "id"

    def get_queryset(self):  # these params are not required, they're just infinitely little/big by default!
        hospital_id = self.kwargs.get("id")
        queryset = Timetable.objects.filter(hospital_id=hospital_id)
        if self.request.method == "GET":
            time_from_param = datetime.fromisoformat(self.request.query_params.get("from", "1970-01-01T00:00:00Z"))
            time_to_param = datetime.fromisoformat(self.request.query_params.get("to", "9999-12-31T23:59:59Z"))
            queryset = queryset.filter(Q(time_from__lte=time_from_param) & Q(time_to_gte=time_from_param) |
                                       Q(time_from_param__gte=time_from_param) & Q(time_to__lte=time_to_param) |
                                       Q(time_from_param__gte=time_from_param) & Q(time_to__gte=time_to_param))
        return queryset

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        for timetable in queryset:
            self.perform_destroy(timetable)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.soft_delete()


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter("from", description="From (timetable is active at this moment of time or "
                                                 "starts after this and before 'from')",
                             location=OpenApiParameter.QUERY,
                             default="1970-01-01T00:00:00Z"),
            OpenApiParameter("to", description="To (timetable is active at this moment of time or "
                                               "ends between 'from' and 'to')",
                             location=OpenApiParameter.QUERY,
                             default="9999-12-31T23:59:59Z")
        ]
    )
)
class GetDeleteTimeTablesByDoctorInPeriodView(ListAPIView, DestroyAPIView):
    """
    Endpoint to retrieve list of all timetables for given doctor in given period

    GET /api/Timetable/Doctor/{id} ?from=<>&to=<>
    """
    permission_classes = [IsAdminOrManagerWithRoleOrGetAndAuthenticated,]
    serializer_class = TimetableSerializer
    lookup_field = "id"

    def get_queryset(self):  # these params are not required, they're just infinitely little/big by default!
        doctor_id = self.kwargs.get("id")
        queryset = Timetable.objects.filter(doctor_id=doctor_id)
        if self.request.method == "GET":
            time_from_param = datetime.fromisoformat(self.request.query_params.get("from", "1970-01-01T00:00:00Z"))
            time_to_param = datetime.fromisoformat(self.request.query_params.get("to", "9999-12-31T23:59:59Z"))
            queryset = queryset.filter(Q(time_from__lte=time_from_param) & Q(time_to_gte=time_from_param) |
                                       Q(time_from_param__gte=time_from_param) & Q(time_to__lte=time_to_param) |
                                       Q(time_from_param__gte=time_from_param) & Q(time_to__gte=time_to_param))
        return queryset

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        for timetable in queryset:
            self.perform_destroy(timetable)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.soft_delete()


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter("from", description="From: (min. appointment START time)",
                             type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
            OpenApiParameter("to", description="To: (max. appointment START time)",
                             type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        ]
    ),
)
class GetTimetablesByHospitalRoomInPeriodView(ListAPIView):
    """
    Endpoint to retrieve list of all timetables for given room in given hospital in given period
    GET /api/Timetable/Hospital/{id}/Room/{room}?from=<>&to=<>
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = TimetableSerializer
    http_method_names = ["get"]
    allowed_methods = ["get"]

    def get_queryset(self):  # these params are not required, they're just infinitely little/big by default!
        time_from_param = datetime.fromisoformat(self.request.query_params.get("from", "1970-01-01T00:00:00Z"))
        time_to_param = datetime.fromisoformat(self.request.query_params.get("to", "9999-12-31T23:59:59Z"))
        hospital_id = self.kwargs.get("id")
        room_name = self.kwargs.get("room")  # TODO: if there must be 1 timetable for 1 hospital room...
        return Timetable.objects.filter(time_from__gte=time_from_param, time_to__lte=time_to_param,
                                        hospital_id=hospital_id, room=room_name)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter("from", description="From: (min. appointment START time)",
                             type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
            OpenApiParameter("to", description="To: (max. appointment START time)",
                             type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        ],
        description="Endpoint for retrieving a list of available time"
                    " marks to appoint to by timetable id.\nGET /api/Timetable/{id}/Appointments"
    ),
    post=extend_schema(
        request=inline_serializer(
            name="AppointmentCreateSerializer",
            fields={
                "time": serializers.DateTimeField()
            }
        ),
        description="Endpoint to create an appointment if the time is available\nPOST /api/Timetable/{id}/Appointments"
    )
)
class GetCreateAppointmentsByTimetableViewSet(APIView):
    """
    - Endpoint for retrieving a list of available time marks to appoint to by timetable id.
    GET /api/Timetable/{id}/Appointments

    - Endpoint to create an appointment if the time is available
    POST /api/Timetable/{id}/Appointments
    """
    permission_classes = [IsAuthenticated,]
    http_method_names = ["get", "post"]
    allowed_methods = ["get", "post"]
    serializer_class = AppointmentSerializer

    def get(self, request, id):
        timetable_id = self.kwargs.get("id")
        timetable_to_analyze = get_object_or_404(Timetable, id=timetable_id)

        result_tickets_list = []  # list of datetime describing available tickets
        """
                           12:30        13:00        13:30        14:00        14:30        15:00
        time_from            |            |            |            |  time_to   X            X
        current_datetime     |            |            |            |     X      X            X
                            free       occupied       free         free  LATE   LATE        LATE
        result: [12:30, 13:30, 14:00]
        """
        current_datetime = timetable_to_analyze.time_from
        while current_datetime < timetable_to_analyze.time_to:
            if not Appointment.objects.filter(timetable=timetable_to_analyze, time=current_datetime).exists():
                result_tickets_list.append(current_datetime.isoformat())
            current_datetime += timedelta(minutes=30)
        return Response(result_tickets_list, status=status.HTTP_200_OK)

    def post(self, request, id):
        post_ = request.data

        # post_ is { time: datetime }

        post_["user_id"] = request.user.id  # user's id is an integer field
        post_["timetable"] = get_object_or_404(Timetable, id=self.kwargs.get("id")).id

        # post_ is { time: datetime, user_id: int, timetable: int }

        serializer = self.serializer_class(data=post_)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAppointmentView(DestroyAPIView):
    """
    Simple delete endoint for Appointment model. Only the user that created it and admins/managers can use it.

    DELETE /api/Appointment/{id}
    """
    permission_classes = [DeleteAppointmentPermission]
    http_method_names = ["delete"]
    allowed_methods = ["delete"]
    serializer_class = AppointmentSerializer
    lookup_field = "id"
    queryset = Appointment.objects.all()

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     # if "Admin" not in request.user.roles and "Manager" not in request.user.roles:
    #     #     if instance.user_id != request.user["id"]:
    #     #         return Response({"details": "You can't delete it! You're not an admin/manager "
    #     #                                     "and you're not the user that created this model."},
    #     #                         status=status.HTTP_403_FORBIDDEN)
    #     super().destroy(request, args, kwargs)
