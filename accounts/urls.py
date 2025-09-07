from django.urls import path
from .views import (
    login_user,
    register_user,
    settings,
    logout_view,
    update_user,
    update_password,
)
from django.contrib.auth import views as auth_views

app_name = "accounts"
urlpatterns = [
    path("login/", login_user, name="login"),
    path("register/", register_user, name="register"),
    path("settings", settings, name="settings"),
    path("logout/", logout_view, name="logout"),
    path("update_user/", update_user, name="update_user"),
    path("update_password/", update_password, name="update_password"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset_form.html",
            email_template_name="accounts/password_reset_email.html",
            subject_template_name="accounts/password_reset_subject.txt",
            success_url="/password_reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url="/reset/done/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
