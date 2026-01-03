from django.db import models
from core.models import Employee, Shift

class AttendanceImport(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to="attendance/imports/")
    status = models.CharField(max_length=20, default="success")  # success/failed/processing
    error_report = models.TextField(blank=True, default="")

    def __str__(self):
        return f"Import {self.id} @ {self.uploaded_at:%Y-%m-%d %H:%M}"

class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ("present", "Present"),
        ("leave", "Leave"),
        ("wfh", "WFH"),
        ("absent", "Absent"),
        ("halfday", "Half-day"),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="present")

    late_minutes = models.IntegerField(default=0)
    early_minutes = models.IntegerField(default=0)
    worked_minutes = models.IntegerField(default=0)

    source_import = models.ForeignKey(AttendanceImport, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ("employee", "date")

    def __str__(self):
        return f"{self.employee} {self.date}"
