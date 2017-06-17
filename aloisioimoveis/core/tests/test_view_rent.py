from django.shortcuts import resolve_url as r
from django.test import TestCase


class RentTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('rent'))

    def test_get(self):
        """GET /alugar/ should return status 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use rent.html"""
        self.assertTemplateUsed(self.response, 'rent.html')
