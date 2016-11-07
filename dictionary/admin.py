from django.contrib import admin
from .models import MedicalTerm, BloodType, DocumentType

admin.site.register(MedicalTerm)
admin.site.register(BloodType)
admin.site.register(DocumentType)
