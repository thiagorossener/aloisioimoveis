from datetime import datetime

from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.properties.models import Land


class LandModelTest(TestCase):
    def setUp(self):
        self.obj = mommy.make(Land)

    def test_create(self):
        """Should create a Land"""
        self.assertTrue(Land.objects.exists())

    def test_created_at(self):
        """Land must have a created_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_updated_at(self):
        """Land must have a updated_at attr"""
        self.assertIsInstance(self.obj.updated_at, datetime)

    def test_str(self):
        """str() must return 'Terreno [id] localizado em [Neightbodhood]/[City]"""
        self.assertEqual('Terreno {} localizado em {}/{}'
                         .format(self.obj.id, self.obj.neighborhood, self.obj.city),
                         str(self.obj))
