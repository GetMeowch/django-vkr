from django import forms
from .models import Document
from .validates import MultipleFileInput
from .formatChecker import ContentTypeRestrictedFileField


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['docs']
        widgets = {
            'docs': MultipleFileInput,
        }
        # file = forms.FileField()
        # files = forms.FileField(required=True, widget=MultipleFileInput)