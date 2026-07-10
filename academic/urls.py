"""Explicit academic API URL routes."""
from django.urls import path

from academic.views import (
    AcademicDashboardView,
    AcademicYearViewSet,
    ClassRoomViewSet,
    HolidayViewSet,
    SchoolDashboardView,
    SectionViewSet,
    TeacherAssignmentViewSet,
)

academic_year_list = AcademicYearViewSet.as_view({"get": "list", "post": "create"})
academic_year_detail = AcademicYearViewSet.as_view({"get": "retrieve", "patch": "partial_update", "put": "update", "delete": "destroy"})
academic_year_current = AcademicYearViewSet.as_view({"get": "current"})

class_list = ClassRoomViewSet.as_view({"get": "list", "post": "create"})
class_detail = ClassRoomViewSet.as_view({"get": "retrieve", "patch": "partial_update", "put": "update", "delete": "destroy"})

section_list = SectionViewSet.as_view({"get": "list", "post": "create"})
section_detail = SectionViewSet.as_view({"get": "retrieve", "patch": "partial_update", "put": "update", "delete": "destroy"})

teacher_assignment_list = TeacherAssignmentViewSet.as_view({"get": "list", "post": "create"})
teacher_assignment_detail = TeacherAssignmentViewSet.as_view({"get": "retrieve", "patch": "partial_update", "put": "update", "delete": "destroy"})
teacher_assignment_remove = TeacherAssignmentViewSet.as_view({"post": "remove"})

holiday_list = HolidayViewSet.as_view({"get": "list", "post": "create"})
holiday_detail = HolidayViewSet.as_view({"get": "retrieve", "patch": "partial_update", "put": "update", "delete": "destroy"})
holiday_calendar = HolidayViewSet.as_view({"get": "calendar"})
holiday_monthly = HolidayViewSet.as_view({"get": "monthly"})
holiday_date_range = HolidayViewSet.as_view({"get": "date_range"})

urlpatterns = [
    path("academic-years/", academic_year_list, name="academic-year-list"),
    path("academic-years/current/", academic_year_current, name="academic-year-current"),
    path("academic-years/<int:pk>/", academic_year_detail, name="academic-year-detail"),
    path("classes/", class_list, name="class-list"),
    path("classes/<int:pk>/", class_detail, name="class-detail"),
    path("sections/", section_list, name="section-list"),
    path("sections/<int:pk>/", section_detail, name="section-detail"),
    path("teacher-assignments/", teacher_assignment_list, name="teacher-assignment-list"),
    path("teacher-assignments/<int:pk>/", teacher_assignment_detail, name="teacher-assignment-detail"),
    path("teacher-assignments/<int:pk>/remove/", teacher_assignment_remove, name="teacher-assignment-remove"),
    path("holidays/", holiday_list, name="holiday-list"),
    path("holidays/calendar/", holiday_calendar, name="holiday-calendar"),
    path("holidays/monthly/", holiday_monthly, name="holiday-monthly"),
    path("holidays/date-range/", holiday_date_range, name="holiday-date-range"),
    path("holidays/<int:pk>/", holiday_detail, name="holiday-detail"),
    path("dashboard/school/", SchoolDashboardView.as_view(), name="school-dashboard"),
    path("dashboard/academic/", AcademicDashboardView.as_view(), name="academic-dashboard"),
]
