from django import forms
from .models import PettyCashFund, PettyCashVoucher, PettyCashBill, BillAllocation, PettyCashReconciliation

class FundForm(forms.ModelForm):
    class Meta:
        model = PettyCashFund
        fields = ["date", "amount_received", "received_from", "reference", "notes"]

class VoucherForm(forms.ModelForm):
    class Meta:
        model = PettyCashVoucher
        fields = ["voucher_no", "date", "paid_to", "purpose", "category", "amount_dispensed", "approved_by", "disbursed_by", "status"]

class BillForm(forms.ModelForm):
    class Meta:
        model = PettyCashBill
        fields = ["bill_no", "vendor", "bill_date", "amount_on_bill", "submitted_by"]

class AllocationForm(forms.ModelForm):
    class Meta:
        model = BillAllocation
        fields = ["bill", "allocated_amount"]

class ReconciliationForm(forms.ModelForm):
    class Meta:
        model = PettyCashReconciliation
        fields = ["period_start", "period_end", "opening_balance", "cash_counted", "notes"]
