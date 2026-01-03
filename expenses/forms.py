from django import forms
from .models import Expense

class ExpenseClaimForm(forms.ModelForm):
    """Used by regular employees to submit claims."""
    class Meta:
        model = Expense
        fields = ["date", "vendor", "category", "amount", "payment_method", "notes"]
