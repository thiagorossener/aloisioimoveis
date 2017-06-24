from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.locations.models import City, Neighborhood
from aloisioimoveis.locations.serializers import NeighborhoodSerializer


class NeighborhoodSerializerTest(TestCase):
    def test_serializer(self):
        """Neighborhood serialization should return dict with id and name"""
        city = mommy.make(City, name='Taubaté')
        neighborhood = mommy.make(Neighborhood, name='Independência', city=city)
        serializer = NeighborhoodSerializer(neighborhood)
        self.assertDictEqual({'id': 1, 'name': 'Independência'},
                             serializer.data)
