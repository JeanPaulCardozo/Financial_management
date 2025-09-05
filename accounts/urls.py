from django.urls import path
from .views import (
    login_user,
    register_user,
    settings,
    logout_view,
    update_user,
    update_password,
)

app_name = "accounts"
urlpatterns = [
    path("login/", login_user, name="login"),
    path("register/", register_user, name="register"),
    path("settings", settings, name="settings"),
    path("logout/", logout_view, name="logout"),
    path("update_user/", update_user, name="update_user"),
    path("update_password/", update_password, name="update_password"),
]
