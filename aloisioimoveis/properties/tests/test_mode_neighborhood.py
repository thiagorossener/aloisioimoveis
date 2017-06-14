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

    def create_city(self):
        city = City(
            name='Taubaté'
        )
        city.save()
        return city
