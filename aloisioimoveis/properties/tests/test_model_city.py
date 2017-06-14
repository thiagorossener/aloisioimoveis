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
