from datetime import datetime

from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.properties.models import Commercial


class CommercialModelTest(TestCase):
    def setUp(self):
        self.obj = mommy.make(Commercial)

    def test_create(self):
        """Should create a Commercial"""
        self.assertTrue(Commercial.objects.exists())

    def test_created_at(self):
        """Commercial must have a created_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_updated_at(self):
        """Commercial must have a updated_at attr"""
        self.assertIsInstance(self.obj.updated_at, datetime)

    def test_str(self):
        """str() must return 'Ponto Comercial [id] localizado em [Neightbodhood]/[City]"""
        self.assertEqual('Ponto Comercial {} localizado em {}/{}'
                         .format(self.obj.id, self.obj.neighborhood, self.obj.city),
                         str(self.obj))
