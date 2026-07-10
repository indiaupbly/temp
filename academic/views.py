from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from academic.models import AcademicYear, ClassRoom, Section, TeacherAssignment, Holiday
from academic.permissions import AcademicPermission
from academic.serializers import AcademicYearSerializer, ClassRoomSerializer, SectionSerializer, TeacherAssignmentSerializer, HolidaySerializer
from academic.selectors import apply_common_filters, restrict_school_queryset
from academic.services import calculate_working_days, get_current_academic_year
from common.responses import success_response
from school.models import School
from school.permissions import user_school_id, is_super_admin
from school.serializers import SchoolSerializer

class BaseAcademicViewSet(ModelViewSet):
    permission_classes = [AcademicPermission]

class AcademicYearViewSet(BaseAcademicViewSet):
    serializer_class = AcademicYearSerializer
    def get_queryset(self): return apply_common_filters(restrict_school_queryset(AcademicYear.objects.select_related("school"), self.request.user), self.request.query_params, ["name"])
    @action(detail=False, methods=["get"], url_path="current")
    def current(self, request):
        qs = self.get_queryset().filter(is_current=True).first()
        return success_response("Fetched successfully.", self.get_serializer(qs).data if qs else None)

class ClassRoomViewSet(BaseAcademicViewSet):
    serializer_class = ClassRoomSerializer
    def get_queryset(self): return apply_common_filters(restrict_school_queryset(ClassRoom.objects.select_related("school","academic_year").prefetch_related("sections"), self.request.user), self.request.query_params, ["class_name"])

class SectionViewSet(BaseAcademicViewSet):
    serializer_class = SectionSerializer
    def get_queryset(self): return apply_common_filters(restrict_school_queryset(Section.objects.select_related("class_room__school","class_room__academic_year"), self.request.user, "class_room__school"), self.request.query_params, ["section_name"])

class TeacherAssignmentViewSet(BaseAcademicViewSet):
    serializer_class = TeacherAssignmentSerializer
    def get_queryset(self): return apply_common_filters(restrict_school_queryset(TeacherAssignment.objects.select_related("teacher","academic_year__school","class_room","section"), self.request.user, "academic_year__school"), self.request.query_params, [])
    @action(detail=True, methods=["post"], url_path="remove")
    def remove(self, request, pk=None):
        obj = self.get_object(); obj.is_active = False; obj.save(update_fields=["is_active"])
        return success_response("Teacher assignment removed successfully.", self.get_serializer(obj).data)

class HolidayViewSet(BaseAcademicViewSet):
    serializer_class = HolidaySerializer
    def get_queryset(self): return apply_common_filters(restrict_school_queryset(Holiday.objects.select_related("school","academic_year"), self.request.user), self.request.query_params, ["title","description","type"])
    @action(detail=False, methods=["get"], url_path="calendar")
    def calendar(self, request): return self.list(request)
    @action(detail=False, methods=["get"], url_path="monthly")
    def monthly(self, request):
        month = request.query_params.get("month"); year = request.query_params.get("year")
        qs = self.get_queryset()
        if month and year: qs = qs.filter(date__month=month, date__year=year)
        return success_response("Fetched successfully.", self.get_serializer(qs, many=True).data)
    @action(detail=False, methods=["get"], url_path="date-range")
    def date_range(self, request): return self.list(request)

class SchoolDashboardView(APIView):
    permission_classes = [AcademicPermission]
    def get(self, request):
        qs = School.objects.all() if is_super_admin(request.user) else School.objects.filter(id=user_school_id(request.user))
        school = qs.first(); current = get_current_academic_year(school) if school else None
        data = {"school": SchoolSerializer(school).data if school else None, "teachers": 0, "students": 0, "classes": school.classes.count() if school else 0, "sections": Section.objects.filter(class_room__school=school).count() if school else 0, "current_academic_year": current.name if current else None, "attendance_threshold": school.attendance_threshold if school else None, "upcoming_holidays": HolidaySerializer(Holiday.objects.filter(school=school).order_by("date")[:5], many=True).data if school else []}
        return success_response("Dashboard fetched successfully.", data)

class AcademicDashboardView(APIView):
    permission_classes = [AcademicPermission]
    def get(self, request):
        school = School.objects.filter(id=user_school_id(request.user)).first() if not is_super_admin(request.user) else School.objects.first()
        current = get_current_academic_year(school) if school else None
        data = {"current_academic_year": current.name if current else None, "classes": ClassRoom.objects.filter(school=school, academic_year=current).count() if current else 0, "sections": Section.objects.filter(class_room__school=school, class_room__academic_year=current).count() if current else 0, "teachers_assigned": TeacherAssignment.objects.filter(academic_year=current, is_active=True).count() if current else 0, "working_days": calculate_working_days(school, current) if current else 0, "holiday_count": Holiday.objects.filter(school=school, academic_year=current).count() if current else 0}
        return success_response("Dashboard fetched successfully.", data)
