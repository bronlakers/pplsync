from django import forms

class AttendanceUploadForm(forms.Form):
    file = forms.FileField(help_text="Upload .xlsx file")
