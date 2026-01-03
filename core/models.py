from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Shift(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    grace_minutes_late = models.PositiveIntegerField(default=0)
    grace_minutes_early = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    employee_code = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=150)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    default_shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.full_name} ({self.employee_code})"

class Category(models.Model):
    KIND_CHOICES = [
        ("pettycash", "Petty Cash"),
        ("expense", "Expense"),
        ("inventory", "Inventory"),
    ]
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("kind", "name")

    def __str__(self):
        return f"{self.get_kind_display()}: {self.name}"
