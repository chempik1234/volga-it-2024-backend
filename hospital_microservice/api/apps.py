import json

from django.apps import AppConfig

import multiprocessing


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
