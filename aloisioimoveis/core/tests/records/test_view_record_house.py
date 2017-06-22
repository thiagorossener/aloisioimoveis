from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.properties.models import House


class RecordHouseViewTest(TestCase):
    def setUp(self):
        self.house = mommy.make(House)
        self.response = self.client.get(r('record_house', self.house.pk))

    def test_get(self):
        """GET /imovel/casa/[pk]/ should return status 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """GET /imovel/casa/[pk]/ must use record.html"""
        self.assertTemplateUsed(self.response, 'record.html')

    def test_context(self):
        """GET /imovel/casa/[pk]/ should load a house with id [pk]"""
        self.assertEqual(self.house, self.response.context['property'])

    def test_404(self):
        """GET /imovel/casa/[invalid_pk]/ should return status 404"""
        response = self.client.get(r('record_house', 234))
        self.assertEqual(404, response.status_code)

    def test_context_with_fields(self):
        """Must have tuple of fields in context"""
        mommy.make(House, pk=2, total_bedroom=1, total_room=1)
        response = self.client.get(r('record_house', 2))
        self.assertIn((0, 1, 'bedroom'), response.context['fields'])
        self.assertIn((1, 1, 'room'), response.context['fields'])

    def test_context_with_cols(self):
        """Must have cols in context"""
        self.assertEqual((0, 1), self.response.context['cols'])
