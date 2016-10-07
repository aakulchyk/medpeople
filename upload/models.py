from django.db import models
import datetime
class Attachment(models.Model):
    file = models.FileField(upload_to='attachments')
    all_content = models.TextField()
    visit_date = models.DateField(default=datetime.date.today())


