from django.test import TestCase
from django.urls import reverse

from django.db import models
from .models import Attachment

class UploadViewTests(TestCase):
    
    def test_done_view(self):
        response = self.client.get(reverse('upload:done'))
        self.assertEqual(response.status_code, 200)
        
    def test_index_view_no_documents(self):
        response = self.client.get(reverse('upload:index'))
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['document_list'], [])
    
    def test_index_view_one_document(self):
        obj = Attachment.objects.create()
        obj.save()
        response = self.client.get(reverse('upload:index'))
        self.assertEqual(response.status_code, 200)
        #self.assertQuerysetEqual(response.context['document_list'], [])
        
        
