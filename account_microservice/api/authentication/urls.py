from django.urls import path

from .views import SignUpView, SignInView, SignOutView
from .jwt_authentication import CustomTokenVerifyView, CustomTokenRefreshView

app_name = "api"

urlpatterns = [
     path('/SignUp', SignUpView.as_view(), name="sign_up"),       # /api/Authantication/SignUp
     path('/SignIn', SignInView.as_view(), name="sign_in"),       # /api/Authantication/SignIn
     path('/SignOut', SignOutView.as_view(), name="sign_out"),    # /api/Authantication/SignOut
     path('/Validate', CustomTokenVerifyView.as_view(),
          name="validate"),                                      # /api/Authantication/Validate - validate accessToken
     path('/Refresh', CustomTokenRefreshView.as_view(),
          name="validate")                                       # /api/Authantication/Refresh - refresh a JWT pair
]
