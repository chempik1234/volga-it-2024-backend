from django.db import models
# from .elasticsearch_documents import VisitIndex


class Visit(models.Model):
    """
    Patient visit model. It has some data that users should be able to search by.
    """

    hospital_id = models.IntegerField(
        verbose_name="ID больницы",
        null=False,
        blank=False,
        unique=False
    )
    patient_id = models.IntegerField(
        verbose_name="ID пациента",
        null=False,
        blank=False,
        unique=False
    )
    doctor_id = models.IntegerField(
        verbose_name="ID врача",
        null=False,
        blank=False,
        unique=False
    )
    date = models.DateTimeField(
        verbose_name="Дата (время) приёма ISO8601",
        null=False,
        blank=False,
        unique=False
    )
    room = models.CharField(
        verbose_name="Название кабинета",  # not the id, cause 1) that's easier
        null=False,                                          # 2) it's still unique for the room (with hospital_id)
        blank=False,
        unique=False,
        max_length=60  # just like in the original model!
    )
    data = models.TextField(
        verbose_name="Данные",
        null=False,
        blank=True
    )

    # def elastic_index(self):
    #     new_document = VisitIndex(
    #         meta={
    #             'id': self.id
    #         },
    #         date=self.date,
    #         room=self.room,
    #         data=self.data
    #     )
    #     new_document.save()
    #     return new_document.to_dict(include_meta=True)
