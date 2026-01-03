from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
import datetime as dt

from .forms import LoginForm
from .utils import in_group
from attendance.models import AttendanceRecord
from pettycash.models import PettyCashVoucher, PettyCashReconciliation
from expenses.models import Expense
from assets.models import Asset
from core.models import Employee

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        if user:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Invalid username/password.")
    return render(request, "core/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    today = dt.date.today()
    first = today.replace(day=1)

    attendance_count = AttendanceRecord.objects.filter(date__gte=first, date__lte=today).count()
    open_vouchers = PettyCashVoucher.objects.filter(status__in=["open", "partially_billed"]).count()
    pending_expenses = Expense.objects.filter(status="submitted").count()
    assets_assigned = Asset.objects.filter(status="assigned").count()

    att_by_status = (
        AttendanceRecord.objects.filter(date__gte=first, date__lte=today)
        .values("status").annotate(c=Count("id"))
    )
    att_status_labels = [x["status"] for x in att_by_status]
    att_status_values = [x["c"] for x in att_by_status]

    late_count = AttendanceRecord.objects.filter(date__gte=first, date__lte=today, late_minutes__gt=0).count()
    early_count = AttendanceRecord.objects.filter(date__gte=first, date__lte=today, early_minutes__gt=0).count()

    exp_by_status = Expense.objects.values("status").annotate(c=Count("id"))
    exp_status_labels = [x["status"] for x in exp_by_status]
    exp_status_values = [x["c"] for x in exp_by_status]

    assets_by_status = Asset.objects.values("status").annotate(c=Count("id"))
    asset_status_labels = [x["status"] for x in assets_by_status]
    asset_status_values = [x["c"] for x in assets_by_status]

    recent_recs = PettyCashReconciliation.objects.order_by("-created_at")[:6]
    rec_labels = [f"{r.period_start:%b %d}–{r.period_end:%b %d}" for r in reversed(recent_recs)]
    rec_variance = [float(r.variance) for r in reversed(recent_recs)]

    employee = Employee.objects.filter(user=request.user).first()

    ctx = {
        "attendance_count": attendance_count,
        "open_vouchers": open_vouchers,
        "pending_expenses": pending_expenses,
        "assets_assigned": assets_assigned,
        "late_count": late_count,
        "early_count": early_count,
        "att_status_labels": att_status_labels,
        "att_status_values": att_status_values,
        "exp_status_labels": exp_status_labels,
        "exp_status_values": exp_status_values,
        "asset_status_labels": asset_status_labels,
        "asset_status_values": asset_status_values,
        "rec_labels": rec_labels,
        "rec_variance": rec_variance,
        "employee_linked": employee is not None,
        "is_hr": in_group(request.user, "HR") or request.user.is_superuser,
        "is_finance": in_group(request.user, "Finance") or request.user.is_superuser,
        "is_inventory": in_group(request.user, "Inventory") or request.user.is_superuser,
    }
    return render(request, "core/dashboard.html", ctx)
