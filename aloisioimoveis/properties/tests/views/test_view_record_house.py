from urllib.parse import urlencode

from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.locations.models import City, Neighborhood
from aloisioimoveis.properties.models import House, Property


class HouseRecordViewTest(TestCase):
    def setUp(self):
        self.house = mommy.make(House)
        self.response = self.client.get(r('records:house', self.house.pk))

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
        response = self.client.get(r('records:house', 234))
        self.assertEqual(404, response.status_code)

    def test_contact_link(self):
        """Must have a link to the contact page"""
        data = [('id', self.house.pk), (Property.TYPE, Property.HOUSE)]
        self.assertContains(self.response, '?'.join([r('contact'), urlencode(data)]))

    def test_html(self):
        """Should show House record data"""
        city = mommy.make(City, name='Taubaté')
        neighborhood = mommy.make(Neighborhood, name='Belém', city=city)
        house = mommy.make(House,
                           num_record=123,
                           intent=Property.RENT,
                           obs='Piscina e churrasqueira',
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
                           total_leisure_area=9,
                           total_suite=10,
                           total_bathroom=11,
                           total_coffe_room=12,
                           total_pantry=13,
                           total_office=14,
                           total_garage=15,
                           )
        response = self.client.get(r('records:house', house.pk))
        contents = [
            ('<h2>ALUGAR</h2>', 1),
            ('Ficha nº 123', 1),
            ('R$ 100,00', 1),
            ('IPTU R$ 45,00', 1),
            ('Belém - Taubaté', 1),
            ('Rua da Amargura, 456', 1),
            ('Piscina e churrasqueira', 1),
            ('1 quarto', 1),
            ('2 quartos de empregada', 1),
            ('3 banheiros de empregada', 1),
            ('4 lavatórios', 1),
            ('5 salas', 1),
            ('6 cozinhas', 1),
            ('7 halls', 1),
            ('8 áreas de serviço', 1),
            ('9 ranchos', 1),
            ('10 suítes', 1),
            ('11 banheiros', 1),
            ('12 copas', 1),
            ('13 despensas', 1),
            ('14 escritórios', 1),
            ('15 vagas de garagem', 1),
            ('no-photos.png', 2),
        ]
        for content, count in contents:
            with self.subTest():
                self.assertContains(response, content, count)

    def test_suite(self):
        """Should show 2 suites and no bedroom"""
        city = mommy.make(City, name='Taubaté')
        neighborhood = mommy.make(Neighborhood, name='Belém', city=city)
        house = mommy.make(House,
                           num_record=123,
                           intent=Property.RENT,
                           obs='',
                           price=100,
                           conditions='',
                           city=city,
                           neighborhood=neighborhood,
                           address='',
                           total_bedroom=0,
                           total_suite=2,
                           )
        response = self.client.get(r('records:house', house.pk))
        contents = [
            ('0 quarto', 0),
            ('2 suítes', 1),
        ]
        for content, count in contents:
            with self.subTest():
                self.assertContains(response, content, count)
