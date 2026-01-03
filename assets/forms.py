from django import forms
from .models import Asset, AssetAssignment
from core.models import Employee

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["asset_tag", "serial_no", "model", "purchase_date", "warranty_end", "condition", "status"]

class AssignForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.filter(is_active=True))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows":3}))
