from django_elasticsearch_dsl_drf import serializers
from .visit_document import VisitDocument


class VisitDocumentSerializer(serializers.DocumentSerializer):
    """Basic serializer for the Visit document."""
    patientId = serializers.IntegerField(source="patient_id")
    hospitalId = serializers.IntegerField(source="hospital_id")
    doctorId = serializers.IntegerField(source="doctor_id")

    class Meta:
        """Meta options."""
        document = VisitDocument
        fields = (
            'id',
            'patientId',
            'hospitalId',
            'doctorId',
            'room',
            'date',
            'data'
        )
