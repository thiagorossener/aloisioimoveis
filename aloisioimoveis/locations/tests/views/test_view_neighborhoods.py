from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.locations.models import City, Neighborhood


class NeighborhoodsViewTest(TestCase):
    def test_get(self):
        """GET /api/locations/neighborhoods?city=1 should return status 200"""
        city = mommy.make(City, name='Tremembé')
        mommy.make(Neighborhood, name='São João', city=city)
        response = self.client.get('/api/locations/neighborhoods', {'city': 1})
        self.assertEqual(200, response.status_code)

    def test_json(self):
        """GET /api/locations/neighborhoods?city=1 should return list of all
        neighborhoods in the city"""
        city = mommy.make(City, name='Tremembé')
        mommy.make(Neighborhood, name='São João', city=city)
        mommy.make(Neighborhood, name='Madalena', city=city)
        response = self.client.get('/api/locations/neighborhoods', {'city': 1})
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             [{'id': 2, 'name': 'Madalena'},
                              {'id': 1, 'name': 'São João'}])

    def test_nonexistent_city(self):
        """GET /api/locations/neighborhoods?city=[nonexistent_pk] should return empty list"""
        response = self.client.get('/api/locations/neighborhoods', {'city': 576})
        self.assertJSONEqual(str(response.content, encoding='utf8'), [])

    def test_invalid_city(self):
        """GET /api/locations/neighborhoods?city=[invalid_pk] should return status 500"""
        response = self.client.get('/api/locations/neighborhoods', {'city': 'bla'})
        self.assertEqual(500, response.status_code)
