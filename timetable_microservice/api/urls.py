from django.urls import path
# ISO 8601 YYYY-MM-DD + 'T' + HH:MM:SS + 'Z'
from .views import (CreateTimetableView,                     # POST /api/Timetable
                    TimetablePutDeleteViewSet,               # PUT DELETE /api/Timetable/{id}
                    # DeleteTimetablesByDoctorView,            # DELETE /api/Timetable/Doctor/{id}
                    # DeleteTimetablesByHospitalView,          # DELETE /api/Timetable/Hospital/{id}
                    GetDeleteTimeTablesByHospitalInPeriodView,
                                                             # GET /api/Timetable/Hospital/{id}?from=<>&to=<>
                                                             # DELETE /api/Timetable/Hospital/{id}
                    GetDeleteTimeTablesByDoctorInPeriodView,
                                                             # GET /api/Timetable/Doctor/{id}?from=<>&to=<>
                                                             # DELETE /api/Timetable/Doctor/{id}
                    GetTimetablesByHospitalRoomInPeriodView, # GET /api/Timetable/Hospital/{id}/Room/{room}?from=^&to=^
                    GetCreateAppointmentsByTimetableViewSet, # GET POST /api/Timetable/{id}/Appointments
                    DeleteAppointmentView                    # DELETE /api/Appointment/{id}
                    )

app_name = "api"


urlpatterns = [
    path("Timetable", CreateTimetableView.as_view(), name="create_timetable"),
    path("Timetable/Doctor/<int:id>", GetDeleteTimeTablesByDoctorInPeriodView.as_view(),
         name="get_delete_timetables_by_doctor"),
    path("Timetable/Hospital/<int:id>", GetDeleteTimeTablesByHospitalInPeriodView.as_view(),
         name="get_delete_timetables_by_hospital"),
    path("Timetable/Hospital/<int:id>/Room/<str:room>", GetTimetablesByHospitalRoomInPeriodView.as_view(),
         name="get_timetables_by_room"),
    path("Appointment/<int:id>", DeleteAppointmentView.as_view(), name="delete_appointment"),
    path("Timetable/<int:id>/Appointments", GetCreateAppointmentsByTimetableViewSet.as_view(),
         name="get_or_create_timetable"),
    path("Timetable/<int:id>", TimetablePutDeleteViewSet.as_view(), name="put_or_delete_timetable")
]
