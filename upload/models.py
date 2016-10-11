from django.db import models
#import datetime
from django.utils import timezone

from dictionary.models import MedicalTerm

class Attachment(models.Model):
    file_attached = models.FileField(upload_to='attachments')
    all_content = models.TextField()
    visit_date = models.DateField(default=timezone.now())
    tags = models.ManyToManyField(MedicalTerm)
    
    def __str__(self):
        return 'File: %s, Uploaded %s' % (str(self.file_attached).split('/')[-1], str(self.visit_date))

    

