from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from api.models import Visit

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@INDEX.doc_type
class VisitDocument(Document):
    """models.py Visit Elasticsearch document."""

    # id = fields.IntegerField(attr='id')

    id = fields.IntegerField(attr='id')
    data = fields.TextField(attr='data')
    date = fields.DateField(attr='date')
    room = fields.TextField(attr='room')
    hospital_id = fields.IntegerField()
    patient_id = fields.IntegerField()
    doctor_id = fields.IntegerField()

    class Django(object):
        model = Visit
