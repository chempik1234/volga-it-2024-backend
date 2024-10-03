from django.urls import path

from .views import DoctorsListView, DoctorByIdView

app_name = "api"

urlpatterns = [
    path('', DoctorsListView.as_view(), name="doctors_list"),               # /api/Doctors
    path('/<int:id>', DoctorByIdView.as_view(), name="doctor_details")       # /api/Doctors/{id}
]
