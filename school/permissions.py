from accounts.models import UserRole


def is_super_admin(user) -> bool:
    return bool(user and user.is_authenticated and (user.is_superuser or user.role == UserRole.SUPER_ADMIN))

def is_school_admin(user) -> bool:
    return bool(user and user.is_authenticated and user.role == UserRole.SCHOOL_ADMIN)

def is_teacher(user) -> bool:
    return bool(user and user.is_authenticated and user.role == UserRole.TEACHER)

def user_school_id(user):
    if not user or not user.is_authenticated:
        return None
    if hasattr(user, "admin_school"):
        return user.admin_school_id if hasattr(user, "admin_school_id") else user.admin_school.id
    assignment = user.class_assignments.filter(is_active=True).select_related("academic_year__school").first() if hasattr(user, "class_assignments") else None
    return assignment.academic_year.school_id if assignment else None
