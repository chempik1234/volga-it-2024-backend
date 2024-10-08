import multiprocessing
import logging
from django.contrib.auth import get_user_model
from django.db import transaction

logger = logging.getLogger(__name__)

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
        logger.info("CREATED ADMIN")
    except Exception:
        logger.info("COULDN'T CREATE ADMIN")
        pass
    try:
        service.create_user("manager", "manager", ["Manager"], is_staff=True, is_superuser=True)
        logger.info("CREATED MANAGER")
    except Exception:
        logger.info("COULDN'T CREATE MANAGER")
        pass
    try:
        service.create_user("doctor", "doctor", ["Doctor"], is_staff=True, is_superuser=True)
        logger.info("CREATED DOCTOR")
    except Exception:
        logger.info("COULDN'T CREATE DOCTOR")
        pass
    try:
        service.create_user("user", "user", ["User"], is_staff=True, is_superuser=True)
        logger.info("CREATED USER")
    except Exception:
        logger.info("COULDN'T CREATE USER")
        pass


# create the 4 default users using multiprocessing
process = multiprocessing.Process(target=create_4_users)
process.start()
