from django_elasticsearch_dsl_drf.filter_backends import FilteringFilterBackend, \
    OrderingFilterBackend, SearchFilterBackend
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .visit_document import VisitDocument
from .serializers import VisitDocumentSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Retrieve a list of documents",
        description="Search endpoint that allows you to retrieve a list of visit documents "
                    "with filtering, searching, and ordering.",
        parameters=[
            OpenApiParameter(name='room', type=str, location=OpenApiParameter.QUERY,
                             required=False, description='Filter by room ID.'),
            OpenApiParameter(name='date', type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY,
                             required=False, description='Filter by visit datetime.'),
            OpenApiParameter(name='hospitalId', type=int, location=OpenApiParameter.QUERY,
                             required=False, description='Filter by hospital ID.'),
            OpenApiParameter(name='patientId', type=int, location=OpenApiParameter.QUERY,
                             required=False, description='Filter by patient ID.'),
            OpenApiParameter(name='doctorId', type=int, location=OpenApiParameter.QUERY,
                             required=False, description='Filter by doctor ID.'),
            OpenApiParameter(name='ordering', type=str, location=OpenApiParameter.QUERY,
                             required=False, description='Specify the ordering of results (e.g., date,-date).'),
            OpenApiParameter(name='search', type=str, location=OpenApiParameter.QUERY,
                             required=False, description='The main field: Search within visit documents.'),
        ],
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific document",
        description="Search endpoint allows to retrieve a specific visit document by ID.",
        parameters=[
            OpenApiParameter(name='id', type=int, location=OpenApiParameter.PATH,
                             required=True),
        ],
    ),
)
class VisitDocumentViewSet(BaseDocumentViewSet):
    document = VisitDocument
    serializer_class = VisitDocumentSerializer
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        SearchFilterBackend,
    ]
    queryset = document.search()
    search_fields = (
        'data',
        'room'
    )
    filter_fields = {
        'id': 'id',
        'room': 'room',
        'data': 'data',
        'date': 'date',
        'hospitalId': 'hospitalId',
        'patientId': 'patientId',
        'doctorId': 'doctorId',
    }
    # Define ordering fields
    ordering_fields = {
        'id': 'id',
        'date': 'date',
        'hospitalId': 'hospitalId',
        'patientId': 'patientId',
        'doctorId': 'doctorId',
    }
