from urllib.parse import urlencode

from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.locations.models import City, Neighborhood
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

    def test_contact_link(self):
        """Must have a link to the contact page"""
        data = [('id', self.land.pk), (Property.TYPE, Property.LAND)]
        self.assertContains(self.response, '?'.join([r('contact'), urlencode(data)]))

    def test_html(self):
        """Should show Land record data"""
        city = mommy.make(City, name='Taubaté')
        neighborhood = mommy.make(Neighborhood, name='Belém', city=city)
        land = mommy.make(Land,
                          num_record=123,
                          intent=Property.BUY,
                          obs='Piscina e churrasqueira',
                          area='150m2',
                          price=100,
                          conditions='IPTU R$ 45,00',
                          city=city,
                          neighborhood=neighborhood,
                          address='Rua da Amargura, 456',
                          )
        response = self.client.get(r('records:land', land.pk))
        contents = [
            ('<h2>COMPRAR</h2>', 1),
            ('Ficha nº 123', 1),
            ('R$ 100,00', 1),
            ('IPTU R$ 45,00', 1),
            ('Belém - Taubaté', 1),
            ('Rua da Amargura, 456', 0),
            ('Piscina e churrasqueira', 1),
            ('Área de 150m2', 1),
        ]
        for content, count in contents:
            with self.subTest():
                self.assertContains(response, content, count)
