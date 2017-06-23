from django.test import TestCase
from django.shortcuts import resolve_url as r
from model_mommy import mommy

from aloisioimoveis.properties.models import Land


class LandRecordViewTest(TestCase):
    def setUp(self):
        self.land = mommy.make(Land)
        self.response = self.client.get(r('record_land', pk=1))

    def test_get(self):
        """GET /imovel/terreno/[pk]/ should return status 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """GET /imovel/terreno/[pk]/ must use record.html"""
        self.assertTemplateUsed(self.response, 'record.html')

    def test_context(self):
        """GET /imovel/terreno/[pk]/ should load a land with id [pk]"""
        self.assertEqual(self.land, self.response.context['property'])

    def test_404(self):
        """GET /imovel/terreno/[invalid_pk]/ should return status 404"""
        response = self.client.get(r('record_land', 234))
        self.assertEqual(404, response.status_code)

    def test_show_area(self):
        """Must show area if property has area"""
        mommy.make(Land, pk=2, area='500m2')
        response = self.client.get(r('record_land', 2))
        self.assertContains(response, '<div class="area">Área de 500m2</div>')
