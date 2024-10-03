from django.db import models


class Timetable(models.Model):
    """
    Timetable model that creates a worktime description for a doctor with his cabinet and hospital
    has a ISO8601 "to-from" time marks, so users can appoint for every 30 minutes of this period since "time_from"
    Mustn't be changed if a patient has appointed to it! This is checked in other places
    """
    hospital_id = models.IntegerField(
        verbose_name="ID больницы",
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
    time_from = models.DateTimeField(
        verbose_name="Начало (без секунд, минуты кратны 30, ISO8601)",
        null=False,
        blank=False,
        unique=False
    )
    time_to = models.DateTimeField(
        verbose_name="Конец (без секунд, минуты кратны 30, ISO8601)",
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


class Appointment(models.Model):
    """
    User appointment model. A patient can appoint to a timetable. A visit lasts 30 minutes, so the timedelta
    between the time mark and timetable's time_from must be a multiple of this period.
    """
    user_id = models.IntegerField(
        verbose_name="ID пользователя",
        unique=True,
        blank=False,
        null=False
    )
    timetable = models.ForeignKey(
        Timetable,
        verbose_name="Родительское расписание",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        unique=False
    )
    time = models.DateTimeField(
        verbose_name="Время приёма",
        blank=False,
        null=False,
        unique=False
    )
