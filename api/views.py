# pip3 install django-rest-framework

from django.shortcuts import render

from django.contrib.auth.models import User, Group
from dictionary.models import MedicalTerm
from upload.models import Document

from rest_framework import viewsets
from .serializers import DocumentListSerializer

class DocumentListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Document.objects.all().order_by('-visit_date')[:20]
    serializer_class = DocumentListSerializer

