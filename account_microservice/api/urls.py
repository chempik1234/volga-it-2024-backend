import multiprocessing

from django.urls import path, include

from . import signals  # signals in this project are made for performing auto-caching and cleaning cache
# and also CASCADE on delete, there're linked models in timetable_microservice!

app_name = 'api'

urlpatterns = [
    path("Authentication", include('api.authentication.urls')),
    path("Accounts", include('api.accounts.urls')),
    path("Doctors", include('api.doctors.urls')),
]
