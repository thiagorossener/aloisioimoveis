from urllib.parse import urlencode

from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.locations.models import City, Neighborhood
from aloisioimoveis.properties.models import Apartment, Property


class ApartmentRecordViewTest(TestCase):
    def setUp(self):
        self.apartment = mommy.make(Apartment)
        self.response = self.client.get(r('records:apartment', pk=1))

    def test_get(self):
        """GET /imovel/apartamento/[pk]/ should return status 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """GET /imovel/apartamento/[pk]/ must use record.html"""
        self.assertTemplateUsed(self.response, 'record.html')

    def test_context(self):
        """GET /imovel/apartamento/[pk]/ should load an apartment with id [pk]"""
        self.assertEqual(self.apartment, self.response.context['property'])

    def test_404(self):
        """GET /imovel/apartamento/[invalid_pk]/ should return status 404"""
        response = self.client.get(r('records:apartment', 234))
        self.assertEqual(404, response.status_code)

    def test_contact_link(self):
        """Must have a link to the contact page"""
        data = [('id', self.apartment.pk), (Property.TYPE, Property.APARTMENT)]
        self.assertContains(self.response, '?'.join([r('contact'), urlencode(data)]))

    def test_html(self):
        """Should show Apartment record data"""
        city = mommy.make(City, name='Taubaté')
        neighborhood = mommy.make(Neighborhood, name='Belém', city=city)
        apartment = mommy.make(Apartment,
                               num_record=123,
                               intent=Property.BUY,
                               obs='Piscina e churrasqueira',
                               area='150m2',
                               price=100,
                               conditions='IPTU R$ 45,00',
                               city=city,
                               neighborhood=neighborhood,
                               address='Rua da Amargura, 456',
                               total_bedroom=1,
                               total_maids_room=2,
                               total_maids_wc=3,
                               total_lavatory=4,
                               total_room=5,
                               total_kitchen=6,
                               total_hall=7,
                               total_service_area=8,
                               total_suite=9,
                               total_bathroom=10,
                               total_coffe_room=11,
                               total_pantry=12,
                               total_office=13,
                               total_garage=14,
                               )
        response = self.client.get(r('records:apartment', apartment.pk))
        contents = [
            ('<h2>COMPRAR</h2>', 1),
            ('Ficha nº 123', 1),
            ('R$ 100,00', 1),
            ('IPTU R$ 45,00', 1),
            ('Belém - Taubaté', 1),
            ('Rua da Amargura, 456', 0),
            ('Piscina e churrasqueira', 1),
            ('Área de 150m2', 1),
            ('1 quarto', 1),
            ('2 quartos de empregada', 1),
            ('3 banheiros de empregada', 1),
            ('4 lavatórios', 1),
            ('5 salas', 1),
            ('6 cozinhas', 1),
            ('7 halls', 1),
            ('8 áreas de serviço', 1),
            ('9 suítes', 1),
            ('10 banheiros', 1),
            ('11 copas', 1),
            ('12 despensas', 1),
            ('13 escritórios', 1),
            ('14 vagas de garagem', 1),
        ]
        for content, count in contents:
            with self.subTest():
                self.assertContains(response, content, count)
