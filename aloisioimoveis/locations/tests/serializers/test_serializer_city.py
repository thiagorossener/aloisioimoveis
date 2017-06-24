from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.locations.models import City
from aloisioimoveis.locations.serializers import CitySerializer


class CitySerializerTest(TestCase):
    def test_serializer(self):
        """City serialization should return dict with id and name"""
        city = mommy.make(City, name='Taubaté')
        serializer = CitySerializer(city)
        self.assertDictEqual({'id': 1, 'name': 'Taubaté'}, serializer.data)
