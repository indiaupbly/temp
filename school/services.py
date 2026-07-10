from django.db import transaction


@transaction.atomic
def soft_delete_school(school, user):
    school.soft_delete(user)
    return school
