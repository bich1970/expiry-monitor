  # models.py
from django.db import models

class ExcelFile(models.Model):
    file = models.FileField(upload_to='')  # No path: uploads to S3 root and uses original filename
    uploaded_at = models.DateTimeField(auto_now_add=True)

