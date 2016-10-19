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
        # str(self.file_attached).split('/')[-1]

        tags = ' '.join(sorted(['['+x.name+']' for x in self.tags.all()])[:20])
        if not tags:
            tags = u'Какие-то каракули'
        description = tags if self.file_attached else u'Файл не загружен'
        return u'%s : %s' % (str(self.visit_date), description)

    

