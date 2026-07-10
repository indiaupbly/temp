from django.conf import settings
from django.db import models
from django.db.models import Q

from academic.constants import HolidayTypeChoices


class AcademicYear(models.Model):
    school = models.ForeignKey("school.School", on_delete=models.CASCADE, related_name="academic_years")
    name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date"]
        constraints = [models.UniqueConstraint(fields=["school", "name"], name="uniq_academic_year_school_name"), models.UniqueConstraint(fields=["school"], condition=Q(is_current=True), name="uniq_current_year_per_school")]
        indexes = [models.Index(fields=["school", "is_current"]), models.Index(fields=["is_active"])]

    def __str__(self): return f"{self.school} - {self.name}"


class ClassRoom(models.Model):
    school = models.ForeignKey("school.School", on_delete=models.CASCADE, related_name="classes")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="classes")
    class_name = models.CharField(max_length=50)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "class_name"]
        constraints = [models.UniqueConstraint(fields=["school", "academic_year", "class_name"], name="uniq_class_school_year_name")]
        indexes = [models.Index(fields=["school", "academic_year", "is_active"])]

    def __str__(self): return self.class_name


class Section(models.Model):
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name="sections")
    section_name = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["section_name"]
        constraints = [models.UniqueConstraint(fields=["class_room", "section_name"], name="uniq_section_class_name")]
        indexes = [models.Index(fields=["class_room", "is_active"])]

    def __str__(self): return f"{self.class_room}-{self.section_name}"


class TeacherAssignment(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="class_assignments")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="teacher_assignments")
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name="teacher_assignments")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="teacher_assignments")
    assigned_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["teacher", "academic_year"], condition=Q(is_active=True), name="uniq_active_teacher_assignment_year")]
        indexes = [models.Index(fields=["teacher", "academic_year", "is_active"])]


class Holiday(models.Model):
    school = models.ForeignKey("school.School", on_delete=models.CASCADE, related_name="holidays")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="holidays")
    date = models.DateField()
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=30, choices=HolidayTypeChoices.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date"]
        constraints = [models.UniqueConstraint(fields=["school", "date"], name="uniq_holiday_school_date")]
        indexes = [models.Index(fields=["school", "academic_year", "date"]), models.Index(fields=["type"])]
