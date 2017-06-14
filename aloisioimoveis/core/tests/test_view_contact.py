from django.test import TestCase
from django.shortcuts import resolve_url as r


class ContactViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('contact'))

    def test_get(self):
        """GET /contato/ should return 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use contact.html"""
        self.assertTemplateUsed(self.response, 'contact.html')
