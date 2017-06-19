from datetime import datetime

from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.properties.models import House


class HouseModelTest(TestCase):
    def setUp(self):
        self.obj = mommy.make(House)

    def test_create(self):
        """Should create a House"""
        self.assertTrue(House.objects.exists())

    def test_created_at(self):
        """House must have a created_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_updated_at(self):
        """House must have a updated_at attr"""
        self.assertIsInstance(self.obj.updated_at, datetime)

    def test_str(self):
        """str() must return 'Casa [id] localizado em [Neightbodhood]/[City]"""
        self.assertEqual('Casa {} localizada em {}/{}'
                         .format(self.obj.id, self.obj.neighborhood, self.obj.city),
                         str(self.obj))

    def test_property_type(self):
        """property_type() must return 'Casa'"""
        self.assertEqual('Casa', self.obj.property_type())
