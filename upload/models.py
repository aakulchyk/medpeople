from django.db import models
from django.utils import timezone

from dictionary.models import MedicalTerm, DocumentType, BloodType
from django.contrib.auth.models import User
from django.urls import reverse

# test p12345678


class Document(models.Model):
    file_attached = models.FileField(upload_to='attachments')
    all_content = models.TextField()
    visit_date = models.DateField(default=timezone.now())
    tags = models.ManyToManyField(MedicalTerm)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    doc_type = models.ForeignKey(DocumentType,
                                 on_delete=models.CASCADE,
                                 default=0)

    def get_absolute_url(self):
        return reverse('upload.pdf_view', args=[self.file_attached])

    class Meta:
        ordering = ['user', 'visit_date']

    def __str__(self):
        tags = ' '.join(sorted(['['+x.name+']' for x in self.tags.all()])[:20])
        if not tags:
            tags = u'Cannot recognize text'
        description = tags if self.file_attached else u'File not loaded'
        return u'%s : %s' % (str(self.visit_date), description)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    birth_date = models.DateField(default='1900/01/01')
    blood_type = models.ForeignKey(BloodType, default=0)

    def __str__(self):
        return u'%s, born %s, blood: %s, %d documents' % (
            self.name,
            str(self.birth_date),
            self.blood_type,
            0
        )
