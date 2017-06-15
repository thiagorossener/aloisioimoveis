from datetime import datetime

from django.test import TestCase
from aloisioimoveis.properties.models import Neighborhood, City


class NeighborhoodModelTest(TestCase):
    def setUp(self):
        self.obj = Neighborhood(
            name='Belém',
            city=self.create_city()
        )
        self.obj.save()

    def test_create(self):
        """Should create a Neighborhood"""
        self.assertTrue(Neighborhood.objects.exists())

    def test_created_at(self):
        """Neighborhood must have created_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_updated_at(self):
        """Neighborhood must have updated_at attr"""
        self.assertIsInstance(self.obj.updated_at, datetime)

    def create_city(self):
        city = City(
            name='Taubaté'
        )
        city.save()
        return city
