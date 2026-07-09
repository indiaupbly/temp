"""Serializers for account APIs."""
from django.contrib.auth import authenticate, password_validation
from rest_framework import serializers

from accounts.models import User
from common.validators import validate_email, validate_password_strength


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "name", "phone_number", "profile_image", "role", "is_active", "date_joined", "updated_at")
        read_only_fields = fields


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[validate_email])
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs: dict) -> dict:
        request = self.context.get("request")
        user = authenticate(request=request, username=attrs["email"], password=attrs["password"])
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")
        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=False, trim_whitespace=False)
    new_password = serializers.CharField(write_only=True, trim_whitespace=False)
    confirm_new_password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_new_password(self, value: str) -> str:
        validate_password_strength(value)
        password_validation.validate_password(value, self.context.get("target_user"))
        return value

    def validate(self, attrs: dict) -> dict:
        request = self.context["request"]
        target_user = self.context["target_user"]
        if attrs["new_password"] != attrs["confirm_new_password"]:
            raise serializers.ValidationError({"confirm_new_password": "New passwords do not match."})
        changing_other_user = request.user.pk != target_user.pk
        if changing_other_user:
            if not request.user.is_staff and not request.user.is_superuser:
                raise serializers.ValidationError("Only admins can change another user's password.")
        elif not target_user.check_password(attrs.get("old_password", "")):
            raise serializers.ValidationError({"old_password": "Old password is incorrect."})
        return attrs


class UserActivationSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()


class EmptySerializer(serializers.Serializer):
    pass
