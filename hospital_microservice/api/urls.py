from xml.etree.ElementInclude import include

from django.urls import path
from rest_framework.routers import DefaultRouter

from views import HospitalsViewSet, HospitalRoomsListView

router = DefaultRouter()
router.register('Hospitals', HospitalsViewSet.as_view({"get": "hospitals"}),
                basename="hospitals")  # /api/Hospitals
router.register('Hospitals/<int:id>', HospitalsViewSet.as_view({"get": "retrieve",
                                                                "post": "create", "put": "update",
                                                                "delete": "destroy"}),
                basename="hospitals")  # /api/Hospitals/{id}
router.register('Hospitals/<int:id>/Rooms', HospitalRoomsListView.as_view())

urlpatterns = [
    path("", include(router.urls))
]
