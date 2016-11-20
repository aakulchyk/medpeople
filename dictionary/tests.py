from django.test import TestCase
from dictionary.models import MedicalTerm


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
