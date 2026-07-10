from datetime import timedelta
from django.db.models import Count
from academic.models import Holiday, AcademicYear


def get_current_academic_year(school):
    return AcademicYear.objects.filter(school=school, is_current=True, is_active=True).first()


def calculate_working_days(school, academic_year, start_date=None, end_date=None) -> int:
    start = start_date or academic_year.start_date; end = end_date or academic_year.end_date
    excluded = set(Holiday.objects.filter(school=school, academic_year=academic_year, date__range=(start, end), is_active=True).values_list("date", flat=True))
    days = 0; current = start
    while current <= end:
        if current not in excluded: days += 1
        current += timedelta(days=1)
    return days


def calculate_attendance_percentage(present_days: int, working_days: int) -> float:
    return round((present_days / working_days) * 100, 2) if working_days else 0.0
