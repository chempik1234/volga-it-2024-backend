import json
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Appointment, Timetable
from .permissions import IsAdminOrManagerWithRole
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


class TimetablePutDeleteViewSet(RetrieveUpdateDestroyAPIView):
    """
    Simple timetable PUT and DELETE endpoint
    PUT DELETE /api/Timetable/{id}
    """
    permission_classes = [IsAdminOrManagerWithRole,]
    serializer_class = TimetableSerializer
    http_method_names = ["put", "delete"]
    allowed_methods = ["put", "delete"]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if Appointment.objects.filter(timetable=instance).exists():
            return Response({"detail": "A timetable that someone has appointed to can't be changed.."},
                            status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, *kwargs)


class DeleteTimetablesByDoctorView(DestroyAPIView):
    """
    Endpoint for deleting all timetables by doctor_id
    DELETE /api/Timetable/Doctor/{id}
    """
    permission_classes = [IsAdminOrManagerWithRole,]
    serializer_class = TimetableSerializer
    http_method_names = ["delete"]
    allowed_methods = ["delete"]

    def delete(self, request, id):
        # id isn't the PK, it's the doctor_id!
        Timetable.objects.filter(doctor_id=id).delete()  # delete everything (0+ rows) with doctor_id equal to <id>
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteTimetablesByHospitalView(DestroyAPIView):
    """
    Endpoint for deleting all timetables by hospital_id
    DELETE /api/Timetable/Hospital/{id}
    """
    permission_classes = [IsAdminOrManagerWithRole,]
    serializer_class = TimetableSerializer
    http_method_names = ["delete"]
    allowed_methods = ["delete"]

    def delete(self, request, id):
        # id isn't the PK, it's the hospital_id!
        Timetable.objects.filter(hospital_id=id).delete()  # delete everything (0+ rows) with hospital_id equal to <id>
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetTimeTablesByHospitalInPeriodView(ListAPIView):
    """
    Endpoint to retrieve list of all timetables for given hospital in given period
    GET /api/Timetable/Hospital/{id} ?from=<>&to=<>
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = TimetableSerializer
    http_method_names = ["get"]
    allowed_methods = ["get"]

    def get_queryset(self):  # these params are not required, they're just infinitely little/big by default!
        time_from_param = datetime.fromisoformat(self.request.query_params.get("from", "1970-01-01T00:00:00Z"))
        time_to_param = datetime.fromisoformat(self.request.query_params.get("to", "9999-12-31T23:59:59Z"))
        hospital_id = self.kwargs.get("id")
        return Timetable.objects.filter(time_from__gte=time_from_param, time_to__lte=time_to_param,
                                        hospital_id=hospital_id)


class GetTimeTablesByDoctorInPeriodView(ListAPIView):
    """
    Endpoint to retrieve list of all timetables for given doctor in given period
    GET /api/Timetable/Doctor/{id} ?from=<>&to=<>
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = TimetableSerializer
    http_method_names = ["get"]
    allowed_methods = ["get"]

    def get_queryset(self):  # these params are not required, they're just infinitely little/big by default!
        time_from_param = datetime.fromisoformat(self.request.query_params.get("from", "1970-01-01T00:00:00Z"))
        time_to_param = datetime.fromisoformat(self.request.query_params.get("to", "9999-12-31T23:59:59Z"))
        doctor_id = self.kwargs.get("id")
        return Timetable.objects.filter(time_from__gte=time_from_param, time_to__lte=time_to_param,
                                        doctor_id=doctor_id)


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


class GetCreateAppointmentsByTimetableViewSet(APIView):
    """
    - Endpoint for retrieving a list of available time marks to appoint to by timetable id.
    GET /api/Timetable/Hospital/{id}/Room/{room}?from=<>&to=<>

    - Endpoint to create an appointment if the time is available
    POST /api/Timetable/{id}/Appointments
    """
    permission_classes = [IsAuthenticated,]
    http_method_names = ["get", "post"]
    allowed_methods = ["get", "post"]

    def get(self, request):
        timetable_id = self.kwargs.get("id")
        timetable_to_analyze = get_object_or_404(Timetable, id=timetable_id)

        result_tickets_list = []  # list of datetime describing available tickets
        """
                           12:30        13:00        13:30        14:00
        time_from            |            |            |            |  time_to   X            X
        current_datetime     |            |            |            |            X            X
                            free       occupied       free         free         LATE         LATE
        result: [12:30, 13:30, 14:00]
        """
        current_datetime = timetable_to_analyze.time_from
        while current_datetime < timetable_to_analyze.time_to:
            if not Appointment.objects.filter(timetable=timetable_to_analyze, time=current_datetime).exists():
                result_tickets_list.append(current_datetime.isoformat())
            current_datetime += timedelta(minutes=30)
        return Response(result_tickets_list, status=status.HTTP_200_OK)

    def post(self, request):
        post_ = request.data

        # post_ is { time: datetime }

        post_["user_id"] = request.user["id"]  # user's id is an integer field       {"id": int, "lastName": str, ...}
        post_["timetable"] = get_object_or_404(Timetable, id=self.kwargs.get("id")).id

        # post_ is { time: datetime, user_id: int, timetable: int }

        serializer = AppointmentSerializer(data=post_)
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
    permission_classes = [IsAuthenticated]
    http_method_names = ["delete"]
    allowed_methods = ["delete"]
    serializer_class = AppointmentSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if "Admin" not in request.user["roles"] and "Manager" not in request.user["roles"]:
            if instance.user_id != request.user["id"]:
                return Response({"details": "You can't delete it! You're not an admin/manager "
                                            "and you're not the user that created this model."},
                                status=status.HTTP_403_FORBIDDEN)
        super().destroy(request, args, kwargs)
