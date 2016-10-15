from django.test import TestCase
from django.urls import reverse

from .models import Attachment

class UploadViewTests(TestCase):
    
    def test_index_view_no_documents(self):
        response = self.client.get(reverse('upload:index'))
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['document_list'], [])
    
    def test_index_view_one_document(self):
        Attachment.objects.create(file_attached="example.pdf")
        response = self.client.get(reverse('upload:index'))
