from django.contrib import admin
from .models import AttendanceRecord, AttendanceImport

admin.site.register(AttendanceImport)

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("employee", "date", "status", "check_in", "check_out", "late_minutes", "early_minutes")
    list_filter = ("status", "date")
    search_fields = ("employee__employee_code", "employee__full_name")
