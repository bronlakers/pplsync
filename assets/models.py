from django.db import models
from core.models import Employee

class Asset(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("assigned", "Assigned"),
        ("retired", "Retired"),
    ]
    asset_tag = models.CharField(max_length=50, unique=True)
    serial_no = models.CharField(max_length=100, blank=True, default="")
    model = models.CharField(max_length=150, blank=True, default="")
    purchase_date = models.DateField(null=True, blank=True)
    warranty_end = models.DateField(null=True, blank=True)
    condition = models.CharField(max_length=150, blank=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")

    def __str__(self):
        return f"{self.asset_tag} ({self.model})"

class AssetAssignment(models.Model):
    asset = models.ForeignKey(Asset, related_name="assignments", on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.asset} -> {self.employee}"
