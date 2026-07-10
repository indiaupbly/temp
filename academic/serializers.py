from rest_framework import serializers
from accounts.models import UserRole
from academic.models import AcademicYear, ClassRoom, Section, TeacherAssignment, Holiday


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta: model = AcademicYear; fields = "__all__"
    def validate(self, attrs):
        if attrs.get("end_date", getattr(self.instance, "end_date", None)) <= attrs.get("start_date", getattr(self.instance, "start_date", None)):
            raise serializers.ValidationError("End date must be after start date.")
        return attrs

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta: model = ClassRoom; fields = "__all__"

class SectionSerializer(serializers.ModelSerializer):
    class Meta: model = Section; fields = "__all__"

class TeacherAssignmentSerializer(serializers.ModelSerializer):
    class Meta: model = TeacherAssignment; fields = "__all__"
    def validate_teacher(self, value):
        if value.role != UserRole.TEACHER: raise serializers.ValidationError("Only teachers can be assigned.")
        return value
    def validate(self, attrs):
        cr = attrs.get("class_room", getattr(self.instance, "class_room", None)); sec = attrs.get("section", getattr(self.instance, "section", None))
        if sec and cr and sec.class_room_id != cr.id: raise serializers.ValidationError("Section must belong to selected class.")
        return attrs

class HolidaySerializer(serializers.ModelSerializer):
    class Meta: model = Holiday; fields = "__all__"
