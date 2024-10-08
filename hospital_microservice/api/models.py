from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Hospital(models.Model):
    """
    Hospital model with name, address and regexed <=15 digits phone number
    """
    name = models.CharField(
        verbose_name="Название больницы",
        unique=False,
        null=False,
        blank=False,
        validators=[MinLengthValidator(1)],
        max_length=120
    )
    address = models.CharField(
        verbose_name="Адрес больницы",
        unique=False,
        null=False,
        blank=False,
        validators=[MinLengthValidator(1)],
        max_length=250
    )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. "
                                         "Up to 15 digits allowed.")
    contact_phone = models.CharField(
        verbose_name="Контактный номер телефона",
        validators=[phone_regex],
        max_length=17,
        blank=False,
        null=False
    )
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    def soft_delete(self):
        self.is_deleted = True
        self.save()


class Room(models.Model):
    """
    Room model, 1 to many with hospitals (even though names repeat, we must keep the room itself unique)
    """
    name = models.CharField(
        verbose_name="Название кабинета",
        unique=False,
        null=False,
        blank=False,
        max_length=60,  # Кабинет слепкоизготовления и стоматологической хиррургии - 56 символов!
        validators=[MinLengthValidator(1)]
    )
    hospital = models.ForeignKey(
        Hospital,
        verbose_name="Больница",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        related_name="rooms"
    )
