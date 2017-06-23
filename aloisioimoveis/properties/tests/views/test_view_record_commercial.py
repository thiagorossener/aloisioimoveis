from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.properties.models import Commercial


class CommercialRecordViewTest(TestCase):
    def setUp(self):
        self.commercial = mommy.make(Commercial)
        self.response = self.client.get(r('records:commercial', pk=1))

    def test_get(self):
        """GET /imovel/comercial/[pk]/ should return status 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """GET /imovel/comercial/[pk]/ must use record.html"""
        self.assertTemplateUsed(self.response, 'record.html')

    def test_context(self):
        """GET /imovel/comercial/[pk]/ should load a commecial with id [pk]"""
        self.assertEqual(self.commercial, self.response.context['property'])

    def test_404(self):
        """GET /imovel/comercial/[invalid_pk]/ should return status 404"""
        response = self.client.get(r('records:commercial', 234))
        self.assertEqual(404, response.status_code)

    def test_context_with_fields(self):
        """Must have tuple of fields in context"""
        mommy.make(Commercial, pk=2, total_room=1, total_kitchen=1)
        response = self.client.get(r('records:commercial', 2))
        self.assertIn((0, 1, 'room'), response.context['fields'])
        self.assertIn((1, 1, 'kitchen'), response.context['fields'])

    def test_context_with_cols(self):
        """Must have cols in context"""
        self.assertEqual((0, 1), self.response.context['cols'])

    def test_show_area(self):
        """Must show area if property has area"""
        mommy.make(Commercial, pk=2, area='320m2')
        response = self.client.get(r('records:commercial', 2))
        self.assertContains(response, '<div class="area">Área de 320m2</div>')
