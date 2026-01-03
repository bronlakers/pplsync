from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from core.utils import in_group
from .models import Expense
from .forms import ExpenseClaimForm

def _can_manage_expenses(user):
    return user.is_superuser or in_group(user, "Finance")

@login_required
def expense_list(request):
    if _can_manage_expenses(request.user):
        expenses = Expense.objects.select_related("created_by").all().order_by("-date")[:300]
        return render(request, "expenses/list.html", {"expenses": expenses, "is_finance_view": True})
    return redirect("expense_my_list")

@login_required
def expense_my_list(request):
    expenses = Expense.objects.filter(created_by=request.user).order_by("-date")[:300]
    return render(request, "expenses/my_list.html", {"expenses": expenses})

@login_required
def expense_create(request):
    form = ExpenseClaimForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        exp = form.save(commit=False)
        exp.created_by = request.user
        exp.status = "submitted"
        exp.save()
        messages.success(request, "Claim submitted for approval.")
        return redirect("expense_my_list")
    return render(request, "expenses/form.html", {"title": "New Expense Claim", "form": form})

@login_required
def expense_approve(request, expense_id):
    if not _can_manage_expenses(request.user):
        messages.error(request, "You don't have permission to approve expenses.")
        return redirect("expense_list")
    exp = get_object_or_404(Expense, id=expense_id)
    exp.status = "approved"
    exp.approved_by = request.user
    exp.save()
    messages.success(request, "Expense approved.")
    return redirect("expense_list")

@login_required
def expense_paid(request, expense_id):
    if not _can_manage_expenses(request.user):
        messages.error(request, "You don't have permission to mark as paid.")
        return redirect("expense_list")
    exp = get_object_or_404(Expense, id=expense_id)
    exp.status = "paid"
    exp.save()
    messages.success(request, "Expense marked as paid.")
    return redirect("expense_list")
