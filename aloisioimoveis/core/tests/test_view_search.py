from django.test import TestCase
from django.shortcuts import resolve_url as r


class SearchViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('search'))

    def test_get(self):
        """GET /buscar/ should return status 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use search.html"""
        self.assertTemplateUsed(self.response, 'search.html')
