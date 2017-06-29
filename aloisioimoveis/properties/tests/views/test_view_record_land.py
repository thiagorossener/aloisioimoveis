from urllib.parse import urlencode

from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.properties.models import Land, Property


class LandRecordViewTest(TestCase):
    def setUp(self):
        self.land = mommy.make(Land)
        self.response = self.client.get(r('records:land', pk=1))

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
        response = self.client.get(r('records:land', 234))
        self.assertEqual(404, response.status_code)

    def test_show_area(self):
        """Must show area if property has area"""
        mommy.make(Land, pk=2, area='500m2')
        response = self.client.get(r('records:land', 2))
        self.assertContains(response, '<div class="area">Área de 500m2</div>')

    def test_contact_link(self):
        """Must have a link to the contact page"""
        data = [('id', self.land.pk), (Property.TYPE, Property.LAND)]
        self.assertContains(self.response, '?'.join([r('contact'), urlencode(data)]))
