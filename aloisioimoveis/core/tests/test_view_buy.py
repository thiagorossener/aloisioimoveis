from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.properties.models import House, Apartment, Commercial, Land


class BuyTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('buy'))

    def test_get(self):
        """GET /comprar/ should return status 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use buy.html"""
        self.assertTemplateUsed(self.response, 'buy.html')


class BuyContextTest(TestCase):
    def setUp(self):
        self.properties_to_buy = self.create_properties([House, Apartment, Commercial, Land],
                                                        intent='comprar',
                                                        quantity_each=3)
        self.properties_to_rent = self.create_properties([House, Apartment, Commercial, Land],
                                                         intent='alugar',
                                                         quantity_each=2)
        response = self.client.get(r('buy'))
        self.properties = response.context['properties']

    def test_all_properties_to_buy(self):
        """Buy page must load all the properties with 'comprar' intent"""
        self.assertEqual(self.properties_to_buy, len(self.properties))

    def test_only_properties_to_buy(self):
        """Buy page must load only properties with 'comprar' intent"""
        for property in self.properties:
            with self.subTest():
                self.assertEqual('comprar', property.intent)

    def create_properties(self, models, intent, quantity_each):
        for model in models:
            mommy.make(model, intent=intent, _quantity=quantity_each)
        return len(models) * quantity_each
