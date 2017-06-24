from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.locations.models import City


class CitiesViewTest(TestCase):
    def test_get(self):
        """GET /api/locations/cities should return status 200"""
        response = self.client.get('/api/locations/cities')
        self.assertEqual(200, response.status_code)

    def test_json(self):
        """GET /api/locations/cities should return json with all cities"""
        mommy.make(City, name='Taubaté')
        mommy.make(City, name='Tremembé')
        response = self.client.get('/api/locations/cities')
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             [{'id': 1, 'name': 'Taubaté'},
                              {'id': 2, 'name': 'Tremembé'}])
