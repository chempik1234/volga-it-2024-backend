from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinLengthValidator
from django.db import models


class Role(models.Model):
    """
    Role model which objects are attached to users in M2M
    """
    name = models.CharField(
        verbose_name="Название роли",
        unique=True,
        max_length=50,
        null=False,
        blank=False,
        validators=[MinLengthValidator(1)]
    )


class CustomUser(AbstractBaseUser):
    """
    Custom user model with username, last and first name and hashed password. Also has roles list that allows to check
    if he's a doctor or maybe an admin (is_staff & is_superuser goes to play roblox)
    """

    username = models.CharField(
        verbose_name='Никнейм',
        max_length=250,
        unique=True,
        null=False,
        blank=False,
        validators=[MinLengthValidator(1)]
    )

    last_name = models.SlugField(
        verbose_name='Фамилия',
        max_length=50,
        unique=False,
        null=False,
        blank=False,
        validators=[MinLengthValidator(1)]
    )

    first_name = models.SlugField(
        verbose_name='Имя',
        max_length=50,
        unique=False,
        null=False,
        blank=False,
        validators=[MinLengthValidator(1)]
    )

    roles = models.ManyToManyField(
        Role,
        verbose_name="Роли",
        related_name="users",
        null=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = (
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)
