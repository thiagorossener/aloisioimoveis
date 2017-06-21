from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.properties.models import House, Apartment, Commercial, Land


class RentListTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('rent'))

    def test_get(self):
        """GET /alugar/ should return status 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use rent_list.html"""
        self.assertTemplateUsed(self.response, 'rent_list.html')


class RentListContextText(TestCase):
    def setUp(self):
        self.properties_to_rent = create_properties([House, Apartment, Commercial, Land],
                                                    intent='alugar',
                                                    quantity_each=3)
        self.properties_to_buy = create_properties([House, Apartment, Commercial, Land],
                                                   intent='comprar',
                                                   quantity_each=2)
        response = self.client.get(r('rent'))
        self.properties = response.context['properties']

    def test_all_properties_to_rent(self):
        """Rent page must load all properties with 'alugar' intent"""
        self.assertEqual(self.properties_to_rent, len(self.properties))

    def test_only_properties_to_rent(self):
        """Rent page must load only properties with 'alugar' intent"""
        for prop in self.properties:
            with self.subTest():
                self.assertEqual('alugar', prop.intent)


class RentListTemplateTest(TestCase):
    def test_show_address(self):
        """Rent template should show property address"""
        mommy.make(House, intent='alugar', address='Rua Silvester, 123')
        response = self.client.get(r('rent'))
        self.assertContains(response, '<div class="rua">')


def create_properties(models, intent, quantity_each):
    for model in models:
        mommy.make(model, intent=intent, _quantity=quantity_each)
    return len(models) * quantity_each
