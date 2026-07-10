from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from accounts.models import UserRole
from school.models import School
from school.permissions import is_super_admin

User = get_user_model()


class SchoolSerializer(serializers.ModelSerializer):
    admin_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=UserRole.SCHOOL_ADMIN), source="admin", write_only=True, required=False)
    admin_email = serializers.EmailField(write_only=True, required=False)
    admin_name = serializers.CharField(write_only=True, required=False)
    admin_phone = serializers.CharField(write_only=True, required=False, allow_blank=True)
    admin = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = School
        fields = "__all__"
        read_only_fields = ("id", "school_code", "created_by", "updated_by", "created_at", "updated_at", "deleted_at")

    def validate(self, attrs):
        request = self.context.get("request")
        if self.instance and not is_super_admin(request.user):
            blocked = {"school_code", "city", "district", "state", "country", "pincode", "address", "board"}
            if blocked.intersection(self.initial_data):
                raise serializers.ValidationError("School admins cannot update school code, location, or board.")
        if not self.instance and not attrs.get("admin") and not self.initial_data.get("admin_email"):
            raise serializers.ValidationError("Select an existing school admin or provide admin_email to create one.")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        request = self.context["request"]
        admin_email = validated_data.pop("admin_email", None)
        admin_name = validated_data.pop("admin_name", "School Admin")
        admin_phone = validated_data.pop("admin_phone", "")
        if not validated_data.get("admin"):
            admin, _ = User.objects.get_or_create(email=admin_email, defaults={"name": admin_name, "phone_number": admin_phone, "role": UserRole.SCHOOL_ADMIN, "is_staff": True})
            validated_data["admin"] = admin
        validated_data["created_by"] = request.user
        validated_data["updated_by"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)
