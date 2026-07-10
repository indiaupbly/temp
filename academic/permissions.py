from rest_framework.permissions import BasePermission, SAFE_METHODS
from school.permissions import is_super_admin, is_school_admin, is_teacher


class AcademicPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if is_super_admin(request.user) or is_school_admin(request.user):
            return True
        return is_teacher(request.user) and request.method in SAFE_METHODS
