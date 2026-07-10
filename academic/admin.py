from django.contrib import admin
from academic.models import AcademicYear, ClassRoom, Section, TeacherAssignment, Holiday

admin.site.register(AcademicYear)
admin.site.register(ClassRoom)
admin.site.register(Section)
admin.site.register(TeacherAssignment)
admin.site.register(Holiday)
