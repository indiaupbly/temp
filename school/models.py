"""School domain models."""
from django.conf import settings
from django.db import models
from django.utils import timezone

from common.validators import validate_email, validate_phone
from school.constants import BoardChoices, SchoolTypeChoices
from school.validators import validate_school_logo


class School(models.Model):
    school_code = models.CharField(max_length=20, unique=True, editable=False)
    school_name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, validators=[validate_email])
    phone_number = models.CharField(max_length=20, unique=True, validators=[validate_phone])
    alternate_phone = models.CharField(max_length=20, blank=True, validators=[validate_phone])
    address = models.TextField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")
    pincode = models.CharField(max_length=12)
    board = models.CharField(max_length=30, choices=BoardChoices.choices)
    school_type = models.CharField(max_length=30, choices=SchoolTypeChoices.choices)
    principal_name = models.CharField(max_length=150)
    principal_phone = models.CharField(max_length=20, validators=[validate_phone])
    principal_email = models.EmailField(validators=[validate_email])
    attendance_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=75.00)
    attendance_start_date = models.DateField(default=timezone.localdate)
    is_active = models.BooleanField(default=True)
    school_logo = models.ImageField(upload_to="schools/logos/", blank=True, null=True, validators=[validate_school_logo])
    timezone = models.CharField(max_length=64, default="Asia/Kolkata")
    admin = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="admin_school")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="schools_created")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="schools_updated")
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["school_name"]
        indexes = [models.Index(fields=["school_code"]), models.Index(fields=["is_active"]), models.Index(fields=["city", "state"])]

    def save(self, *args, **kwargs):
        if self.pk:
            old = type(self).objects.only("school_code").get(pk=self.pk)
            self.school_code = old.school_code
        elif not self.school_code:
            last = type(self).objects.order_by("-id").first()
            next_id = (last.id + 1) if last else 1
            self.school_code = f"SCH{next_id:04d}"
        super().save(*args, **kwargs)

    def soft_delete(self, user=None) -> None:
        self.is_active = False
        self.deleted_at = timezone.now()
        self.updated_by = user
        self.save(update_fields=["is_active", "deleted_at", "updated_by", "updated_at"])

    def __str__(self) -> str:
        return self.school_name
