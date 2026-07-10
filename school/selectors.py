from django.db.models import Q
from school.models import School
from school.permissions import is_super_admin, user_school_id


def visible_schools(user):
    qs = School.objects.select_related("admin", "created_by", "updated_by").filter(deleted_at__isnull=True)
    if is_super_admin(user): return qs
    sid = user_school_id(user)
    return qs.filter(id=sid) if sid else qs.none()


def apply_school_filters(qs, params):
    search = params.get("search") or params.get("q")
    if search: qs = qs.filter(Q(school_name__icontains=search) | Q(school_code__icontains=search) | Q(email__icontains=search) | Q(city__icontains=search))
    for field in ["is_active", "city", "district", "state", "board", "school_type"]:
        if field in params: qs = qs.filter(**{field: params[field]})
    ordering = params.get("ordering")
    return qs.order_by(ordering) if ordering else qs
