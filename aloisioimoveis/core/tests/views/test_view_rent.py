from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy
from model_mommy.recipe import Recipe

from aloisioimoveis.locations.models import City, Neighborhood
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
    def setUp(self):
        self.city = mommy.make(City, name='Taubaté')
        self.neighborhood = mommy.make(Neighborhood, name='Belém', city=self.city)
        self.props = [self.build_property(prop) for prop in [House, Apartment, Commercial, Land]]
        self.response = self.client.get(r('rent'))

    def test_html(self):
        """Rent list template should show data"""
        contents = [
            ('Casa', 1),
            ('Apartamento', 1),
            ('Ponto Comercial', 1),
            ('Terreno', 1),
            ('Rua Silvester, 123', 4),
            ('R$ 100,00', 4),
            ('IPTU R$ 45,00', 4),
            ('Belém - Taubaté', 4),
            ('4 quartos', 2),
            ('3 suítes', 2),
            ('2 banheiros', 2),
            ('1 vaga de garagem', 2),
            ('Área de 120m2', 2),
            ('Propriedade com piscina e churrasqueira', 4),
        ]
        for prop in self.props:
            contents.append((prop.get_absolute_url(), 2))
        for content, count in contents:
            with self.subTest():
                self.assertContains(self.response, content, count)

    def build_property(self, model):
        prop = Recipe(model,
                      intent=Property.RENT,
                      address='Rua Silvester, 123',
                      price=100,
                      conditions='IPTU R$ 45,00',
                      neighborhood=self.neighborhood,
                      city=self.city,
                      obs='Propriedade com piscina e churrasqueira',
                      )
        if model is House or model is Apartment:
            prop = prop.extend(total_bedroom=4,
                               total_suite=3,
                               total_bathroom=2,
                               total_garage=1,
                               ).make()
        else:
            prop = prop.extend(area='120m2').make()
        return prop


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
