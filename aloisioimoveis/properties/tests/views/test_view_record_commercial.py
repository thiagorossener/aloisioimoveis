from urllib.parse import urlencode

from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.locations.models import City, Neighborhood
from aloisioimoveis.properties.models import Commercial, Property


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

    def test_contact_link(self):
        """Must have a link to the contact page"""
        data = [('id', self.commercial.pk), (Property.TYPE, Property.COMMERCIAL)]
        self.assertContains(self.response, '?'.join([r('contact'), urlencode(data)]))

    def test_html(self):
        """Should show Commercial record data"""
        city = mommy.make(City, name='Taubaté')
        neighborhood = mommy.make(Neighborhood, name='Belém', city=city)
        commercial = mommy.make(Commercial,
                                num_record=123,
                                intent=Property.RENT,
                                obs='Piscina e churrasqueira',
                                area='150m2',
                                price=100,
                                conditions='IPTU R$ 45,00',
                                city=city,
                                neighborhood=neighborhood,
                                address='Rua da Amargura, 456',
                                total_room=1,
                                total_kitchen=2,
                                total_office=3,
                                total_bathroom=4,
                                total_garage=5,
                                total_service_area=6,
                                )
        response = self.client.get(r('records:commercial', commercial.pk))
        contents = [
            ('<h2>ALUGAR</h2>', 1),
            ('Ficha nº 123', 1),
            ('R$ 100,00', 1),
            ('IPTU R$ 45,00', 1),
            ('Belém - Taubaté', 1),
            ('Rua da Amargura, 456', 1),
            ('Piscina e churrasqueira', 1),
            ('Área de 150m2', 1),
            ('1 sala', 1),
            ('2 cozinhas', 1),
            ('3 escritórios', 1),
            ('4 banheiros', 1),
            ('5 vagas de garagem', 1),
            ('6 áreas de serviço', 1),
        ]
        for content, count in contents:
            with self.subTest():
                self.assertContains(response, content, count)
