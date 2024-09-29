from xml.etree.ElementInclude import include

from django.urls import path
from rest_framework.routers import DefaultRouter

from views import DoctorsListView, DoctorByIdView

router = DefaultRouter()
router.register('Doctors', DoctorsListView.as_view(), basename="doctors_list")  # /api/Authantication/SignUp
router.register('Doctors/<int:id>', DoctorByIdView.as_view(), basename="doctor_details")  # /api/Authantication/SignIn

urlpatterns = [
    path("", include(router.urls))
]
