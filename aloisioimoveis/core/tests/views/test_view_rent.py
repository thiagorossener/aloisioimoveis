from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.properties.models import House, Apartment, Commercial, Land, Property


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
                                                    intent=Property.RENT,
                                                    quantity_each=3)
        self.properties_to_buy = create_properties([House, Apartment, Commercial, Land],
                                                   intent=Property.BUY,
                                                   quantity_each=2)
        response = self.client.get(r('rent'))
        self.properties = response.context['properties']

    def test_all_properties_to_rent(self):
        """Rent page must load all properties with 'alugar' intent"""
        self.assertEqual(self.properties_to_rent, self.properties.paginator.count)

    def test_only_properties_to_rent(self):
        """Rent page must load only properties with 'alugar' intent"""
        for prop in self.properties:
            with self.subTest():
                self.assertEqual(Property.RENT, prop.intent)


class RentListTemplateTest(TestCase):
    def test_show_address(self):
        """Rent template should show property address"""
        mommy.make(House, intent=Property.RENT, address='Rua Silvester, 123')
        response = self.client.get(r('rent'))
        self.assertContains(response, '<div class="rua">')


class RentListPaginationTest(TestCase):
    def test_load_10_properties_per_page(self):
        """Rent page must load at maximum 10 properties per page"""
        properties = self.get_properties_to_rent_list(page=1)
        self.assertEqual(10, len(properties))

    def test_second_page(self):
        """Rent page must load 2 properties on second page"""
        properties = self.get_properties_to_rent_list(page=2)
        self.assertEqual(2, len(properties))

    def test_invalid_page(self):
        """Rent page must load the first page when param 'pagina' is invalid"""
        properties = self.get_properties_to_rent_list(page='bla')
        self.assertEqual(1, properties.number)

    def test_nonexistent_page(self):
        """Rent page must load the last page when the page doesn't exist"""
        properties = self.get_properties_to_rent_list(page=10)
        self.assertEqual(2, properties.number)

    def get_properties_to_rent_list(self, page=None):
        create_properties([House, Apartment, Commercial, Land],
                          intent=Property.RENT,
                          quantity_each=3)
        response = self.client.get(r('rent'), {'pagina': page})
        return response.context['properties']


class RentListSortingTest(TestCase):
    def test_sort_by_most_recent(self):
        """Should return properties sorted by most recent"""
        p1, p2, p3, p4 = self.properties_with_prices([House, Apartment, Commercial, Land],
                                                     [0]*4)
        expected_order = [p4, p3, p2, p1]

        response = self.client.get(r('rent'))
        properties = response.context['properties'].object_list

        self.assertSequenceEqual(expected_order, properties)

    def test_sort_by_lowest_price(self):
        """Should return properties sorted by lowest price"""
        p1, p2, p3, p4 = self.properties_with_prices([House, Apartment, Commercial, Land],
                                                     [2, 3, 1, 4])
        expected_order = [p3, p1, p2, p4]

        response = self.client.get(r('rent'), {'ordem': 'preco'})
        properties = response.context['properties'].object_list

        self.assertSequenceEqual(expected_order, properties)

    def test_sort_by_highest_price(self):
        """Should return properties sorted by highest price"""
        p1, p2, p3, p4 = self.properties_with_prices([House, Apartment, Commercial, Land],
                                                     [4, 2, 3, 1])
        expected_order = [p1, p3, p2, p4]

        response = self.client.get(r('rent'), {'ordem': '-preco'})
        properties = response.context['properties'].object_list

        self.assertSequenceEqual(expected_order, properties)

    @staticmethod
    def properties_with_prices(models, prices):
        result = []
        for index, model in enumerate(models):
            result.append(mommy.make(model, intent=Property.RENT, price=prices[index]))
        return result


class RentListParamsInContextTest(TestCase):
    def test_get_params(self):
        """Rent list should load params in context"""
        params = {'pagina': '1', 'ordem': 'preco'}
        response = self.client.get(r('rent'), params)
        self.assertEqual(params, response.context['params'])


def create_properties(models, intent, quantity_each):
    for model in models:
        mommy.make(model, intent=intent, _quantity=quantity_each)
    return len(models) * quantity_each
