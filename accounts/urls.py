from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView,)
from .views import (
        # GithubOauthSignInView,
        # GoogleOauthSignInview,
        LoginUserView,
        LogoutApiView,
        PasswordResetConfirm,
        PasswordResetRequestView,
        ProfileDetail,
        RegisterInstutionView,
        RegisterUserView,
        SetNewPasswordView, 
        VerifyUserEmail)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name="register-user"),
    path("register/instution/", RegisterInstutionView.as_view(), name="register-inst"),
    path('verify-email/', VerifyUserEmail.as_view(), name="verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginUserView.as_view(), name='login-user'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='reset-password-confirm'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
    path('profile/<int:user_id>/', ProfileDetail.as_view(), name='profile-detail'),
    path('logout/', LogoutApiView.as_view(), name='logout'),
#social media authication 
    # path('google/', GoogleOauthSignInview.as_view(), name='google'),
    # path('github/', GithubOauthSignInView.as_view(), name='github')

]