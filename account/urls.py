from django.contrib import admin
from django.urls import path
from .views import (
    UserRegistrationView,
    LoginUserRegistrationView,
    UserProfileView,
    ChangePasswordUserView,
    SendNotifyPasswordByEmailUserView,
    UserResetPasswordView,
)

urlpatterns = [
    path("register", UserRegistrationView.as_view(), name="register"),
    path("login", LoginUserRegistrationView.as_view(), name="login"),
    path("profile", UserProfileView.as_view(), name="profile"),
    path("change-password", ChangePasswordUserView.as_view(), name="change_password"),
    path(
        "send-email-change-password",
        SendNotifyPasswordByEmailUserView.as_view(),
        name="seng_email_password",
    ),
    path(
        "reset-password/<uid>/<token>",
        UserResetPasswordView.as_view(),
        name="reset_password",
    ),
]
