from django.contrib.auth import get_user_model
from django.db.models import Value, Q
from django.db.models.functions import Concat
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account_microservice.api.serializers import CustomUserSerializer

User = get_user_model()


class DoctorsListView(ListAPIView):
    """
    Doctors list endpoint. Basically, it's just the users list but with the Doctor role.
    GET /api/Doctors
    """
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated,]
    http_method_names = ['GET']
    allowed_methods = ["GET"]

    def get_queryset(self):  # from and count affect the queryset, so it's regenerated with every query
        from_index = int(self.request.query_params.get('from', 0))  # no one said if params are required
        count = int(self.request.query_params.get('count', 10))  # so I made default values: Doctors from 0-10
        name_filter = self.request.query_params.get("nameFilter", "").replace(' ', '')  # same for the name filter

        found_queryset = (User.objects  # the filter is full name, but the field order isn't determined
                          .filter(roles__name="Doctor")
                          .annotate(full_name_1=Concat('last_name', 'first_name'))  # so both ways are used
                          .annotate(full_name_2=Concat('first_name', 'last_name'))
                          .filter(Q(full_name_1__icontains=name_filter) | Q(full_name_2__icontains=name_filter)))

        return found_queryset[from_index:from_index + count]  # cut the doctors queryset


class DoctorByIdView(RetrieveAPIView):
    """
    Doctor details endpoint. Basically, it's just the user-by-id but with the Doctor role.
    GET /api/Doctors/{id}
    """
    serializer_class = CustomUserSerializer
    queryset = User.objects.filter(roles__name="Doctor")
    permission_classes = [IsAuthenticated,]
    http_method_names = ['GET']
    allowed_methods = ["GET"]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()  # get the doctor by id that is retrieved automatically
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
