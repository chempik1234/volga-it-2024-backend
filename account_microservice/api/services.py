from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class UserService:
    def __init__(self):
        pass

    def create_user(self, username, password, roles, is_staff, is_superuser):
        from .models import Role
        with transaction.atomic():
            user = User()
            user.username = username
            user.first_name = username
            user.last_name = username
            user.set_password(password)
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()
            for role_name in roles:
                role, created = Role.objects.get_or_create(name=role_name)
                user.roles.add(role)


def create_4_users():
    service = UserService()
    try:
        service.create_user("admin", "admin", ["Admin"], True, True)
    except Exception:
        pass
    try:
        service.create_user("manager", "manager", ["Manager"], is_staff=True, is_superuser=True)
    except Exception:
        pass
    try:
        service.create_user("doctor", "doctor", ["Doctor"], is_staff=True, is_superuser=True)
    except Exception:
        pass
    try:
        service.create_user("user", "user", ["User"], is_staff=True, is_superuser=True)
    except Exception:
        pass
