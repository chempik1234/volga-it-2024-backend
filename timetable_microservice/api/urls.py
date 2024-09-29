from django.urls import path, include
from rest_framework.routers import DefaultRouter
# ISO 8601 YYYY-MM-DD + 'T' + HH:MM:SS + 'Z'
from views import (CreateTimetableView,                     # POST /api/Timetable
                   TimetablePutDeleteViewSet,               # PUT DELETE /api/Timetable/{id}
                   DeleteTimetablesByDoctorView,            # DELETE /api/Timetable/Doctor/{id}
                   DeleteTimetablesByHospitalView,          # DELETE /api/Timetable/Hospital/{id}
                   GetTimeTablesByHospitalInPeriodView,     # GET /api/Timetable/Hospital/{id}?from=<>&to=<>
                   GetTimeTablesByDoctorInPeriodView,       # GET /api/Timetable/Doctor/{id}?from=<>&to=<>
                   GetTimetablesByHospitalRoomInPeriodView, # GET /api/Timetable/Hospital/{id}/Room/{room}?from=<>&to=<>
                   GetCreateAppointmentsByTimetableViewSet, # GET POST /api/Timetable/{id}/Appointments
                   DeleteAppointmentView                    # DELETE /api/Appointment/{id}
                   )

app_name = "api"

router = DefaultRouter()
router.register("Timetable", CreateTimetableView.as_view())
router.register("Timetable/<int:id>", TimetablePutDeleteViewSet.as_view({'put': 'update', 'delete': 'destroy'}))
router.register("Timetable/Doctor/<int:id>", DeleteTimetablesByDoctorView.as_view())
router.register("Timetable/Hospital/<int:id>", DeleteTimetablesByHospitalView.as_view())
router.register("Timetable/Doctor/<int:id>", GetTimeTablesByDoctorInPeriodView.as_view())
router.register("Timetable/Hospital/<int:id>", GetTimeTablesByHospitalInPeriodView.as_view())
router.register("Timetable/Hospital/<int:id>/Room/<str:room>", GetTimetablesByHospitalRoomInPeriodView.as_view())
router.register("Timetable/<int:id>/Appointments", GetCreateAppointmentsByTimetableViewSet.as_view({'get': "get",
                                                                                                    "post": "post"}))
router.register("Appointment/<int:id>", DeleteAppointmentView.as_view())

urlpatterns = [
    path('', include(router.urls))
]
