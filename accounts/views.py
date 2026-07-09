"""Authentication API views."""
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError

from accounts.models import User
from accounts.serializers import (
    ChangePasswordSerializer,
    EmptySerializer,
    LoginSerializer,
    UserActivationSerializer,
    UserSerializer,
)
from accounts.services import (
    change_user_password,
    login_user,
    logout_user,
    refresh_user_tokens,
    set_user_active_status,
)
from accounts.utils import delete_token_cookie, set_token_cookie
from common.responses import error_response, success_response, updated_response


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = login_user(serializer.validated_data["user"])
        response = success_response(
            "Login successful.", {"user": UserSerializer(result["user"]).data}, status.HTTP_200_OK
        )
        set_token_cookie(response, settings.JWT_ACCESS_COOKIE, result["tokens"]["access"])
        set_token_cookie(response, settings.JWT_REFRESH_COOKIE, result["tokens"]["refresh"])
        return response


class LogoutView(GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        logout_user(request.COOKIES.get(settings.JWT_REFRESH_COOKIE))
        response = success_response("Logout successful.", None, status.HTTP_200_OK)
        delete_token_cookie(response, settings.JWT_ACCESS_COOKIE)
        delete_token_cookie(response, settings.JWT_REFRESH_COOKIE)
        return response


class RefreshView(GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        try:
            tokens = refresh_user_tokens(request.COOKIES.get(settings.JWT_REFRESH_COOKIE))
        except TokenError as exc:
            return error_response(str(exc), None, status.HTTP_401_UNAUTHORIZED)
        response = success_response("Token refreshed successfully.", None, status.HTTP_200_OK)
        set_token_cookie(response, settings.JWT_ACCESS_COOKIE, tokens["access"])
        set_token_cookie(response, settings.JWT_REFRESH_COOKIE, tokens["refresh"])
        return response


class MeView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return success_response("Profile fetched successfully.", {"user": self.get_serializer(request.user).data})


class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_target_user(self):
        user_id = self.kwargs.get("user_id")
        if user_id is None:
            return self.request.user
        return get_object_or_404(User, pk=user_id)

    def post(self, request, *args, **kwargs):
        target_user = self.get_target_user()
        serializer = self.get_serializer(data=request.data, context={"request": request, "target_user": target_user})
        serializer.is_valid(raise_exception=True)
        change_user_password(target_user, serializer.validated_data["new_password"], changed_by=request.user)
        return updated_response("Password changed successfully.")


class UserActivationView(GenericAPIView):
    serializer_class = UserActivationSerializer
    permission_classes = (IsAdminUser,)

    def patch(self, request, user_id, *args, **kwargs):
        target_user = get_object_or_404(User, pk=user_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        changed = set_user_active_status(
            target_user,
            serializer.validated_data["is_active"],
            changed_by=request.user,
        )
        action = "activated" if target_user.is_active else "deactivated"
        message = f"User account {action} successfully." if changed else f"User account is already {action}."
        return updated_response(message, {"user": UserSerializer(target_user).data})

    def post(self, request, user_id, *args, **kwargs):
        return self.patch(request, user_id, *args, **kwargs)
