from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from src.users.views import (UserRegisterCreateAPIView, CheckActivationCodeGenericAPIView, ResetPasswordView,
                             ResetPasswordConfirmView, UserUpdateView)

urlpatterns = [
    path('register', UserRegisterCreateAPIView.as_view()),
    path('register-activate-code', CheckActivationCodeGenericAPIView.as_view()),
    path('reset-password', ResetPasswordView.as_view()),
    path('reset-password-confirm', ResetPasswordConfirmView.as_view()),
    path('login', TokenObtainPairView.as_view()),
    path('login-refresh', TokenRefreshView.as_view()),
    path('profile', UserUpdateView.as_view(), name='user-update'),
]