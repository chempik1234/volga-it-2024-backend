from xml.etree.ElementInclude import include

from django.urls import path
from rest_framework.routers import DefaultRouter

from views import SignUpView, SignInView, SignOutView
from jwt_authentication import CustomTokenVerifyView, CustomTokenRefreshView

router = DefaultRouter()
router.register('SignUp', SignUpView.as_view(), basename="sign_up")  # /api/Authantication/SignUp
router.register('SignIn', SignInView.as_view(), basename="sign_in")  # /api/Authantication/SignIn
router.register('SignOut', SignOutView.as_view(), basename="sign_out")  # /api/Authantication/SignOut
router.register('Validate', CustomTokenVerifyView.as_view(),
                basename="validate")  # /api/Authantication/Validate - validate accessToken
router.register('Refresh', CustomTokenRefreshView.as_view(),
                basename="validate")  # /api/Authantication/Refresh - refresh a JWT pair

urlpatterns = [
    path("", include(router.urls))
]
