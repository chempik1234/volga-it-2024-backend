import multiprocessing

from django.urls import path

from .views import HospitalsViewSet, HospitalRoomsListView

# EXECUTE ON STARTUP
from . import signals  # signals in this project are made for performing auto-caching and cleaning cache
# and also CASCADE on delete, there're linked models in timetable_microservice!

app_name = "api"


urlpatterns = [
    path('Hospitals', HospitalsViewSet.as_view({"get": "hospitals",                         # /api/Hospitals
                                                "post": "create"}), name="hospitals"),
    path('Hospitals/<int:id>', HospitalsViewSet.as_view({"get": "retrieve",                 # /api/Hospitals/{id}
                                                         "put": "update",
                                                         "delete": "destroy"}),
         name="hospitals"),
    path('Hospitals/<int:id>/Rooms', HospitalRoomsListView.as_view(),                       # /api/Hospitals/{id}/Rooms
         name="rooms_by_hospital")
]
