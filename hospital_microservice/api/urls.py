from django.urls import path

from .views import HospitalsViewSet, HospitalRoomsListView

app_name = "api"

urlpatterns = [
    path('Hospitals', HospitalsViewSet.as_view({"get": "hospitals"}), name="hospitals"),    # /api/Hospitals
    path('Hospitals/<int:id>', HospitalsViewSet.as_view({"get": "retrieve",                 # /api/Hospitals/{id}
                                                         "post": "create", "put": "update",
                                                         "delete": "destroy"}),
         name="hospitals"),
    path('Hospitals/<int:id>/Rooms', HospitalRoomsListView.as_view(),                       # /api/Hospitals/{id}/Rooms
         name="rooms_by_hospital")
]
