from datetime import datetime

from django.test import TestCase
from aloisioimoveis.properties.models import City


class CityModelTest(TestCase):
    def setUp(self):
        self.obj = City(
            name='Taubaté'
        )
        self.obj.save()

    def test_create(self):
        """Should create a City"""
        self.assertTrue(City.objects.exists())

    def test_created_at(self):
        """City must have created_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_updated_at(self):
        """City must have updated_at attr"""
        self.assertIsInstance(self.obj.updated_at, datetime)
