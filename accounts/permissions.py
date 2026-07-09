"""Role-based permissions for accounts."""
from rest_framework.permissions import BasePermission

from accounts.models import UserRole


class HasRolePermission(BasePermission):
    roles: tuple[str, ...] = ()

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.role in self.roles)


class IsSuperAdmin(HasRolePermission):
    roles = (UserRole.SUPER_ADMIN,)


class IsSchoolAdmin(HasRolePermission):
    roles = (UserRole.SCHOOL_ADMIN,)


class IsTeacher(HasRolePermission):
    roles = (UserRole.TEACHER,)


class IsSchoolAdminOrTeacher(HasRolePermission):
    roles = (UserRole.SCHOOL_ADMIN, UserRole.TEACHER)
