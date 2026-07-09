"""Authentication API views."""
from django.conf import settings
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError

from accounts.serializers import EmptySerializer, LoginSerializer, UserSerializer
from accounts.services import login_user, logout_user, refresh_user_tokens
from accounts.utils import delete_token_cookie, set_token_cookie
from common.responses import error_response, success_response


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

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

    def post(self, request, *args, **kwargs):
        logout_user(request.COOKIES.get(settings.JWT_REFRESH_COOKIE))
        response = success_response("Logout successful.", None, status.HTTP_200_OK)
        delete_token_cookie(response, settings.JWT_ACCESS_COOKIE)
        delete_token_cookie(response, settings.JWT_REFRESH_COOKIE)
        return response


class RefreshView(GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = (AllowAny,)

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
