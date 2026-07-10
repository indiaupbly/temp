"""Reusable model choices."""
from django.db import models


class Gender(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    OTHER = "OTHER", "Other"


class AttendanceStatus(models.TextChoices):
    PRESENT = "PRESENT", "Present"
    ABSENT = "ABSENT", "Absent"


class DayType(models.TextChoices):
    WORKING = "WORKING", "Working Day"
    HOLIDAY = "HOLIDAY", "Holiday"
    WEEKEND = "WEEKEND", "Weekend"
    EVENT = "EVENT", "Event"
