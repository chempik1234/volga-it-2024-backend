from django.urls import path, include
from rest_framework.routers import DefaultRouter
from views import MeView, UpdateAccountView, AdminAccountsViewSet

router = DefaultRouter()
router.register('Me', MeView.as_view(), basename="me")  # /api/Accounts/Me
router.register('Update', UpdateAccountView.as_view(), basename="update_account")  # /api/Accounts/Update

router.register('', AdminAccountsViewSet.as_view(
    {'get': 'list', 'post': 'create'}),
                basename="sign_out")  # /api/Accounts/
router.register('<int:id>', AdminAccountsViewSet.as_view(
    {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
                basename="sign_out")  # /api/Accounts/{id}

urlpatterns = [
    path("", include(router.urls))
]
