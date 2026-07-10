from django.contrib import admin
from school.models import School

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("school_code", "school_name", "email", "phone_number", "is_active")
    list_filter = ("is_active", "board", "school_type", "state")
    search_fields = ("school_code", "school_name", "email", "phone_number")
    readonly_fields = ("school_code", "created_at", "updated_at", "deleted_at")
