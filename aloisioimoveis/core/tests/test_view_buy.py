from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.properties.models import House, Apartment, Commercial, Land


class BuyListTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('buy'))

    def test_get(self):
        """GET /comprar/ should return status 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use buy.html"""
        self.assertTemplateUsed(self.response, 'buy_list.html')


class BuyListContextTest(TestCase):
    def setUp(self):
        self.properties_to_buy = create_properties([House, Apartment, Commercial, Land],
                                                   intent='comprar',
                                                   quantity_each=3)
        self.properties_to_rent = create_properties([House, Apartment, Commercial, Land],
                                                    intent='alugar',
                                                    quantity_each=2)
        response = self.client.get(r('buy'))
        self.properties = response.context['properties']

    def test_all_properties_to_buy(self):
        """Buy page must load all the properties with 'comprar' intent"""
        self.assertEqual(self.properties_to_buy, self.properties.paginator.count)

    def test_only_properties_to_buy(self):
        """Buy page must load only properties with 'comprar' intent"""
        for property in self.properties:
            with self.subTest():
                self.assertEqual('comprar', property.intent)


class BuyListPaginationTest(TestCase):
    def test_load_10_properties_per_page(self):
        """Buy page must load at maximum 10 properties per page"""
        properties = self.get_properties_to_buy_list()
        self.assertEqual(10, len(properties))

    def test_second_page(self):
        """Buy page must load 2 properties on second page"""
        properties = self.get_properties_to_buy_list(page=2)
        self.assertEqual(2, len(properties))

    def test_invalid_page(self):
        """Buy page must load the first page when param 'pagina' is invalid"""
        properties = self.get_properties_to_buy_list(page='bla')
        self.assertEqual(1, properties.number)

    def test_nonexistent_page(self):
        """Buy page must load the last page when the page doesn't exist"""
        properties = self.get_properties_to_buy_list(page=10)
        self.assertEqual(2, properties.number)

    def get_properties_to_buy_list(self, page=None):
        create_properties([House, Apartment, Commercial, Land],
                          intent='comprar',
                          quantity_each=3)
        response = self.client.get(r('buy'), {'pagina': page})
        return response.context['properties']


def create_properties(models, intent, quantity_each):
    for model in models:
        mommy.make(model, intent=intent, _quantity=quantity_each)
    return len(models) * quantity_each
