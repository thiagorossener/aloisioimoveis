from django.test import TestCase


class CompanyViewTest(TestCase):
    def test_get(self):
        """GET /empresa/ should return status 200"""
        response = self.client.get('/empresa/')
        self.assertEqual(200, response.status_code)

    def test_template(self):
        """Must use company.html"""
        response = self.client.get('/empresa/')
        self.assertTemplateUsed(response, 'company.html')
