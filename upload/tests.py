# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Document
from upload.ocr import pdf_ocr
from upload.ocr import OcrThread
from upload.analyze import AnalyzeThread
from dictionary.models import MedicalTerm


class UploadViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.c = Client()
        cls.c.login(username='test', password='p12345678')

    def test_index_view_with_login_required(self):
        response = self.c.get(reverse('upload:index'))
        self.assertRedirects(response, '/login/?next=%s' % reverse('upload:index'))

        response = self.c.get(response.url)
        self.assertEqual(response.status_code, 200)

    def test_done_view(self):
        response = self.c.get(reverse('upload:done'))
        self.assertEqual(response.status_code, 302)

        response = self.c.get(response.url)
        self.assertEqual(response.status_code, 200)

    def test_post_document(self):
        response = self.c.get(reverse('upload:index'))
        self.assertEqual(response.status_code, 302)

        f = open('attachments/example.pdf', 'rb')
        response = self.c.post(response.url, {'attachments': [f, ]})
        f.close()

        self.assertEqual(response.status_code, 200)

    def test_index_view_one_document(self):
        pass


class OcrTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.filename = 'attachments/test.pdf'
        cls.thread = OcrThread([])

    def test_ocr(self):
        pdf_ocr(self.filename)

    def test_extract(self):
        text = u'((((($$$$))\nкровь \\\\ \n (кишки) !@#$%^&&*()\n\n\nрадость'
        newtext = self.thread.extractAllWordsFromText(text)
        self.assertEqual(newtext, u'кровь\nкишки\nрадость')


class AnalyzerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create()
        cls.doc = Document.objects.create(user=cls.user)
        cls.thread = AnalyzeThread(cls.doc)

    def test_search_tags(self):
        term1 = MedicalTerm.objects.create(name=u'кровь')
        term2 = MedicalTerm.objects.create(name=u'молоко')
        term3 = MedicalTerm.objects.create(name=u'диарея')
        tags = self.thread.search_for_tags('test test test кровь c молоком и кишки testtest')
        self.assertEqual(term1 in tags, True)
        self.assertEqual(term2 in tags, True)
        self.assertEqual(term3 in tags, False)
