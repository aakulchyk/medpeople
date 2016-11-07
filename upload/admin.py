from django.contrib import admin

from .models import Document, Patient

admin.site.register(Document)
admin.site.register(Patient)
