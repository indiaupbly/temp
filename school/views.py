from django.db.models import Count, Q
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.viewsets import ModelViewSet

from accounts.models import UserRole
from common.responses import deleted_response, success_response
from school.models import School
from school.permissions import is_super_admin
from school.selectors import apply_school_filters, visible_schools
from school.serializers import SchoolSerializer
from school.services import soft_delete_school


class SchoolPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated: return False
        if is_super_admin(request.user): return True
        return request.method in SAFE_METHODS


class SchoolViewSet(ModelViewSet):
    serializer_class = SchoolSerializer
    permission_classes = [SchoolPermission]
    search_fields = ["school_name", "school_code", "email", "city"]
    ordering_fields = ["school_name", "school_code", "created_at", "is_active"]

    def get_queryset(self):
        return apply_school_filters(visible_schools(self.request.user), self.request.query_params)

    def destroy(self, request, *args, **kwargs):
        soft_delete_school(self.get_object(), request.user)
        return deleted_response("School deleted successfully.")

    @action(detail=False, methods=["get"], url_path="active")
    def active(self, request):
        qs = self.filter_queryset(self.get_queryset().filter(is_active=True))
        page = self.paginate_queryset(qs)
        if page is not None: return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return success_response("Fetched successfully.", self.get_serializer(qs, many=True).data)

    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        return self.list(request)

    @action(detail=False, methods=["get"], url_path="statistics")
    def statistics(self, request):
        qs = visible_schools(request.user)
        data = {"total_schools": qs.count(), "active_schools": qs.filter(is_active=True).count(), "inactive_schools": qs.filter(is_active=False).count(), "teachers": 0, "students": 0, "classes": sum(s.classes.count() for s in qs.prefetch_related("classes")), "sections": 0}
        data["sections"] = sum(c.sections.count() for s in qs.prefetch_related("classes__sections") for c in s.classes.all())
        return success_response("Statistics fetched successfully.", data)
