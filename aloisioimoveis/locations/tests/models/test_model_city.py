from datetime import datetime

from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.properties.models import City


class CityModelTest(TestCase):
    def setUp(self):
        self.obj = mommy.make(City)

    def test_create(self):
        """Should create a City"""
        self.assertTrue(City.objects.exists())

    def test_created_at(self):
        """City must have created_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_updated_at(self):
        """City must have updated_at attr"""
        self.assertIsInstance(self.obj.updated_at, datetime)

    def test_str(self):
        """str() must return city name"""
        self.assertEqual(self.obj.name, str(self.obj))
