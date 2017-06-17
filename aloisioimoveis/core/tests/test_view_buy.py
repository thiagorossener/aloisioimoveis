from django.shortcuts import resolve_url as r
from django.test import TestCase


class BuyTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('buy'))

    def test_get(self):
        """GET /comprar/ should return status 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use buy.html"""
        self.assertTemplateUsed(self.response, 'buy.html')
