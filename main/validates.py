from django.core.exceptions import ValidationError
from django import forms
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

def validate_file(value):
    value= str(value)
    if value.endswith(".pdf") != True and value.endswith(".doc") != True and value.endswith(".docx") != True:
        raise ValidationError("Only PDF and Word Documents can be uploaded")
    else:
        return value