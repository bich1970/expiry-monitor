from django import forms
from .models import ExcelFile

class UploadExcelForm(forms.ModelForm):
    class Meta:
        model = ExcelFile
        fields = ['file']
