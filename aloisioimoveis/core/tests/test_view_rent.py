from django.test import TestCase


class RentTest(TestCase):
    def test_get(self):
        """GET /alugar/ should return status 200"""
        response = self.client.get('/alugar/')
        self.assertEqual(200, response.status_code)

    def test_template(self):
        """Must use rent.html"""
        response = self.client.get('/alugar/')
        self.assertTemplateUsed(response, 'rent.html')
