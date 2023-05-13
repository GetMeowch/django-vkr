from django.db import models
from django.core.validators import FileExtensionValidator

from .formatChecker import ContentTypeRestrictedFileField
from .validates import validate_file

class Document(models.Model):
    docs = ContentTypeRestrictedFileField(upload_to = "Uploaded Files/", null=True, blank=False, content_types=['application/msword', 'application/pdf', 'vnd.openxmlformats-officedocument.wordprocessingml.document'], max_upload_size=5242880)
