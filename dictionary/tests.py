from django.test import TestCase
from dictionary.models import MedicalTerm
from dictionary.models import DocumentType


class MedicalTermTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.o = MedicalTerm.objects
        cls.terms = [
            cls.o.create(name=u'кровь'),
            cls.o.create(name=u'молоко'),
            cls.o.create(name=u'кишки')
        ]

    def test_get_filters_by_names(self):
        names = ['кровь', 'молоко']
        self.assertEqual(MedicalTerm.objectsByNames(names),
                         [self.terms[0], self.terms[1]])


class DocumentTypeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.t = DocumentType.objects.create()
        cls.tt = DocumentType.objects.create(
            type = DocumentType.SYNEVO_ANALYSIS_TABLE
        )

    def defaultTypeTest(self):
        self.assertEqual(self.t, DocumentType.COMMON_RECIPE, True)
        self.assertEqual(self.t, DocumentType.COMMON_DIAGNOSIS, False)

    def isTableTest(self):
        self.assertEqual(self.t.isTable(), False)
        self.assertEqual(self.tt.isTable(), True)

