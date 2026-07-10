from django.db.models import Q
from school.permissions import is_super_admin, user_school_id


def restrict_school_queryset(qs, user, school_field="school"):
    if is_super_admin(user): return qs
    sid = user_school_id(user)
    return qs.filter(**{f"{school_field}_id": sid}) if sid else qs.none()


def apply_common_filters(qs, params, search_fields=()):
    search = params.get("search") or params.get("q")
    if search and search_fields:
        q = Q()
        for f in search_fields: q |= Q(**{f"{f}__icontains": search})
        qs = qs.filter(q)
    if "is_active" in params: qs = qs.filter(is_active=params["is_active"])
    if params.get("start_date"): qs = qs.filter(date__gte=params["start_date"])
    if params.get("end_date"): qs = qs.filter(date__lte=params["end_date"])
    ordering = params.get("ordering")
    return qs.order_by(ordering) if ordering else qs
