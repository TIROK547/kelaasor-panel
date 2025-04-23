from django.urls import path
from .views import VerifyCodeView, CreateUserView, GetVerificationCodeView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("get-code", GetVerificationCodeView.as_view()),
    path("sing-up", CreateUserView.as_view()),
    path("verify-code", VerifyCodeView.as_view()),
    path("get-token", TokenObtainPairView.as_view()),
    path("refresh-token", TokenRefreshView.as_view()),
]