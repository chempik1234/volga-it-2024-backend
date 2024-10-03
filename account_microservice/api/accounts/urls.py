from django.urls import path
from .views import MeView, UpdateAccountView, AdminAccountsViewSet

app_name = "api"

urlpatterns = [
    path('/Me', MeView.as_view(), name="me"),                                                      # /api/Accounts/Me
    path('/Update', UpdateAccountView.as_view(), name="update_account"),                           # /api/Accounts/Update

    path('', AdminAccountsViewSet.as_view({'get': 'list', 'post': 'create'}), name="sign_out"),   # /api/Accounts/
    path('/<int:id>', AdminAccountsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name="sign_out")                                                                         # /api/Accounts/{id}
]
