"""Account URL routes."""
from django.urls import path

from accounts.views import ChangePasswordView, LoginView, LogoutView, MeView, RefreshView, UserActivationView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("users/<int:user_id>/change-password/", ChangePasswordView.as_view(), name="admin-change-password"),
    path("users/<int:user_id>/activation/", UserActivationView.as_view(), name="admin-user-activation"),
]
