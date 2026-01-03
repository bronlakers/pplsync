from django.contrib import admin
from .models import Employee, Shift, Department, Branch, Category

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_code", "full_name", "department", "branch", "is_active")
    search_fields = ("employee_code", "full_name")

admin.site.register(Shift)
admin.site.register(Department)
admin.site.register(Branch)
admin.site.register(Category)
