from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAdminOrAuthenticatedAndGET
from .models import Hospital
from .serializers import HospitalSerializer, RoomSerializer


@extend_schema_view(
    hospitals=extend_schema(
        parameters=[
            OpenApiParameter("from", description="Selection start (not by id!)",
                             type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
            OpenApiParameter("count", description="Selection size (not by id!)",
                             type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
        ]
    )
)
class HospitalsViewSet(ModelViewSet):
    """
    ViewSet for admin accounts CRUD with roles creation support
    """
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [IsAdminOrAuthenticatedAndGET,]

    @action(detail=False, methods=["get"])
    def hospitals(self, request):
        """
        Hospitals list endpoint (from and count are query params, they limit the performed selection)
        GET /api/Hospitals ?from &count
        """
        from_ = int(request.query_params.get('from', 0))
        count = int(request.query_params.get('count', 10))
        hospitals = Hospital.objects.all()[from_:from_ + count]
        serializer = HospitalSerializer(hospitals, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.soft_destroy()


class HospitalRoomsListView(ListAPIView):
    """
    Rooms list by hospital's id endpoint.
    GET /api/Hospitals/{id}/Rooms
    """
    permission_classes = [IsAuthenticated]
    allowed_methods = ["get"]
    http_method_names = ["get"]
    serializer_class = RoomSerializer

    def get_queryset(self):
        hospital_id = int(self.request.kwargs.get('id'))
        try:
            hospital = Hospital.objects.get(id=hospital_id)
            return hospital.rooms.all()
        except Hospital.DoesNotExist:
            raise NotFound(f"Hospital not found by this id: '{hospital_id}'")
