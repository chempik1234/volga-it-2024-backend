from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path("Authentication", include('api.authentications.urls')),
    path("Accounts", include('api.accounts.urls')),
    path("Doctors", include('api.doctors.urls')),
]