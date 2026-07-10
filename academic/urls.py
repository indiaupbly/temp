from django.urls import path
from rest_framework.routers import DefaultRouter
from academic.views import AcademicDashboardView, AcademicYearViewSet, ClassRoomViewSet, HolidayViewSet, SchoolDashboardView, SectionViewSet, TeacherAssignmentViewSet

router = DefaultRouter()
router.register("academic-years", AcademicYearViewSet, basename="academic-year")
router.register("classes", ClassRoomViewSet, basename="class")
router.register("sections", SectionViewSet, basename="section")
router.register("teacher-assignments", TeacherAssignmentViewSet, basename="teacher-assignment")
router.register("holidays", HolidayViewSet, basename="holiday")
urlpatterns = router.urls + [path("dashboard/school/", SchoolDashboardView.as_view()), path("dashboard/academic/", AcademicDashboardView.as_view())]
