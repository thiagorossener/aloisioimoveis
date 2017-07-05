from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy
from model_mommy.recipe import Recipe

from aloisioimoveis.locations.models import City, Neighborhood
from aloisioimoveis.properties.models import House, Property, Apartment, Commercial, Land


class SearchViewTest(TestCase):
    def setUp(self):
        mommy.make(House, intent=Property.RENT)
        self.response = self.client.get(r('search'),
                                        {Property.INTENT: Property.RENT,
                                         Property.TYPE: Property.HOUSE})

    def test_get(self):
        """GET /buscar/ should return status 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use search.html"""
        self.assertTemplateUsed(self.response, 'search.html')


class SearchTemplateTest(TestCase):
    def setUp(self):
        self.city = mommy.make(City, name='Taubaté')
        self.neighborhood = mommy.make(Neighborhood, name='Belém', city=self.city)

    def test_html_to_house_search(self):
        """Result list template for House search should show data"""
        house = self.build_property(House, Property.BUY)
        response = self.client.get(r('search'), {Property.INTENT: Property.BUY,
                                                 Property.TYPE: Property.HOUSE})
        contents = [
            ('Casa', 1),
            ('Rua Silvester, 123', 0),
            ('R$ 100,00', 1),
            ('IPTU R$ 45,00', 1),
            ('Belém - Taubaté', 1),
            ('4 quartos', 1),
            ('3 suítes', 1),
            ('2 banheiros', 1),
            ('1 vaga de garagem', 1),
            (house.get_absolute_url(), 2),
            ('Propriedade com piscina e churrasqueira', 1),
        ]
        self.assertContents(response, contents)

    def test_html_to_apartment_search(self):
        """Result list template for Apartment search should show data"""
        apartment = self.build_property(Apartment, Property.RENT)
        response = self.client.get(r('search'), {Property.INTENT: Property.RENT,
                                                 Property.TYPE: Property.APARTMENT})
        contents = [
            ('Apartamento', 1),
            ('Rua Silvester, 123', 1),
            ('R$ 100,00', 1),
            ('IPTU R$ 45,00', 1),
            ('Belém - Taubaté', 1),
            ('4 quartos', 1),
            ('3 suítes', 1),
            ('2 banheiros', 1),
            ('1 vaga de garagem', 1),
            (apartment.get_absolute_url(), 2),
            ('Propriedade com piscina e churrasqueira', 1),
        ]
        self.assertContents(response, contents)

    def test_html_to_commercial_search(self):
        """Result list template for Commercial search should show data"""
        commercial = self.build_property(Commercial, Property.RENT)
        response = self.client.get(r('search'), {Property.INTENT: Property.RENT,
                                                 Property.TYPE: Property.COMMERCIAL})
        contents = [
            ('Ponto Comercial', 1),
            ('Rua Silvester, 123', 1),
            ('R$ 100,00', 1),
            ('IPTU R$ 45,00', 1),
            ('Belém - Taubaté', 1),
            ('Área de 120m2', 1),
            (commercial.get_absolute_url(), 2),
            ('Propriedade com piscina e churrasqueira', 1),
        ]
        self.assertContents(response, contents)

    def test_html_to_land_search(self):
        """Result list template for Land search should show data"""
        land = self.build_property(Land, Property.BUY)
        response = self.client.get(r('search'), {Property.INTENT: Property.BUY,
                                                 Property.TYPE: Property.LAND})
        contents = [
            ('Terreno', 1),
            ('Rua Silvester, 123', 0),
            ('R$ 100,00', 1),
            ('IPTU R$ 45,00', 1),
            ('Belém - Taubaté', 1),
            ('Área de 120m2', 1),
            (land.get_absolute_url(), 2),
            ('Propriedade com piscina e churrasqueira', 1),
        ]
        self.assertContents(response, contents)

    def assertContents(self, response, contents):
        for content, count in contents:
            with self.subTest():
                self.assertContains(response, content, count)

    def build_property(self, model, intent):
        prop = Recipe(model,
                      intent=intent,
                      address='Rua Silvester, 123',
                      price=100,
                      conditions='IPTU R$ 45,00',
                      neighborhood=self.neighborhood,
                      city=self.city,
                      obs='Propriedade com piscina e churrasqueira'
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


class IntentSearchTest(TestCase):
    def setUp(self):
        self.house_to_rent = mommy.make(House, intent=Property.RENT)
        self.house_to_buy = mommy.make(House, intent=Property.BUY)

    def test_property_to_rent(self):
        """Search should return a property to rent only"""
        response = self.client.get(r('search'), {Property.INTENT: Property.RENT,
                                                 Property.TYPE: Property.HOUSE})
        self.assertIn(self.house_to_rent, response.context['results'])
        self.assertNotIn(self.house_to_buy, response.context['results'])

    def test_property_to_buy(self):
        """Search should return a property to buy only"""
        response = self.client.get(r('search'), {Property.INTENT: Property.BUY,
                                                 Property.TYPE: Property.HOUSE})
        self.assertNotIn(self.house_to_rent, response.context['results'])
        self.assertIn(self.house_to_buy, response.context['results'])

    def test_house_invalid_intent(self):
        """Should return status 404"""
        response = self.client.get(r('search'), {Property.INTENT: 'invalid',
                                                 Property.TYPE: Property.HOUSE})
        self.assertEqual(404, response.status_code)


class PropertyTypeSearchTest(TestCase):
    def setUp(self):
        self.house = mommy.make(House, intent=Property.RENT)
        self.apartment = mommy.make(Apartment, intent=Property.RENT)
        self.commercial = mommy.make(Commercial, intent=Property.RENT)
        self.land = mommy.make(Land, intent=Property.RENT)

    def test_house(self):
        """Search should return only a house"""
        results = self.get_results(Property.HOUSE)
        self.assertIn(self.house, results)
        self.assertNotIn(self.apartment, results)
        self.assertNotIn(self.commercial, results)
        self.assertNotIn(self.land, results)

    def test_apartment(self):
        """Search should return only an apartment"""
        results = self.get_results(Property.APARTMENT)
        self.assertNotIn(self.house, results)
        self.assertIn(self.apartment, results)
        self.assertNotIn(self.commercial, results)
        self.assertNotIn(self.land, results)

    def test_commercial(self):
        """Search should return only a commercial"""
        results = self.get_results(Property.COMMERCIAL)
        self.assertNotIn(self.house, results)
        self.assertNotIn(self.apartment, results)
        self.assertIn(self.commercial, results)
        self.assertNotIn(self.land, results)

    def test_land(self):
        """Search should return only a land"""
        results = self.get_results(Property.LAND)
        self.assertNotIn(self.house, results)
        self.assertNotIn(self.apartment, results)
        self.assertNotIn(self.commercial, results)
        self.assertIn(self.land, results)

    def test_invalid(self):
        """Should return status 404"""
        response = self.client.get(r('search'),
                                   {Property.TYPE: 'invalid',
                                    Property.INTENT: Property.RENT})
        self.assertEqual(404, response.status_code)

    def get_results(self, property_type):
        response = self.client.get(r('search'),
                                   {Property.TYPE: property_type,
                                    Property.INTENT: Property.RENT})
        return response.context['results']


class CitySearchTest(TestCase):
    def setUp(self):
        self.city1 = mommy.make(City)
        self.city2 = mommy.make(City)
        self.house1 = mommy.make(House, intent=Property.BUY, city=self.city1)
        self.house2 = mommy.make(House, intent=Property.BUY, city=self.city2)

    def test_all_cities(self):
        """Should return properties from all cities"""
        results = self.get_results(city=Property.ALL_CITIES)
        self.assertIn(self.house1, results)
        self.assertIn(self.house2, results)

    def test_one_city(self):
        """Should return properties from one city"""
        results = self.get_results(city=self.city1.pk)
        self.assertIn(self.house1, results)
        self.assertNotIn(self.house2, results)

    def test_invalid_city(self):
        """Should return properties from all cities when city is invalid"""
        results = self.get_results(city='invalid')
        self.assertIn(self.house1, results)
        self.assertIn(self.house2, results)

    def get_results(self, city):
        response = self.client.get(r('search'),
                                   {Property.TYPE: Property.HOUSE,
                                    Property.INTENT: Property.BUY,
                                    Property.CITY: city})
        return response.context['results']


class NeighborhoodSearchTest(TestCase):
    def setUp(self):
        self.city1 = mommy.make(City)
        self.city2 = mommy.make(City)

        self.neighborhood1 = mommy.make(Neighborhood, city=self.city1)
        self.neighborhood2 = mommy.make(Neighborhood, city=self.city1)

        self.house1 = mommy.make(House, intent=Property.RENT,
                                 neighborhood=self.neighborhood1, city=self.city1)
        self.house2 = mommy.make(House, intent=Property.RENT,
                                 neighborhood=self.neighborhood2, city=self.city1)
        self.house3 = mommy.make(House, intent=Property.RENT, city=self.city2)

    def test_all_cities_all_neighborhoods(self):
        """Should return all the properties from all the cities"""
        results = self.get_results(city=Property.ALL_CITIES,
                                   neighborhood=Property.ALL_NEIGHBORHOODS)
        self.assertIn(self.house1, results)
        self.assertIn(self.house2, results)
        self.assertIn(self.house3, results)

    def test_one_city_all_neighborhoods(self):
        """Should return all the properties from all the cities"""
        results = self.get_results(city=self.city1.pk,
                                   neighborhood=Property.ALL_NEIGHBORHOODS)
        self.assertIn(self.house1, results)
        self.assertIn(self.house2, results)
        self.assertNotIn(self.house3, results)

    def test_one_city_one_neighborhood(self):
        """Should return all the properties from all the cities"""
        results = self.get_results(city=self.city1.pk,
                                   neighborhood=self.neighborhood1.pk)
        self.assertIn(self.house1, results)
        self.assertNotIn(self.house2, results)
        self.assertNotIn(self.house3, results)

    def test_invalid_neighborhood(self):
        """Should return the properties from all the city neighborhoods when it's invalid"""
        results = self.get_results(city=self.city1.pk,
                                   neighborhood='invalid')
        self.assertIn(self.house1, results)
        self.assertIn(self.house2, results)
        self.assertNotIn(self.house3, results)

    def get_results(self, city, neighborhood):
        response = self.client.get(r('search'),
                                   {Property.TYPE: Property.HOUSE,
                                    Property.INTENT: Property.RENT,
                                    Property.CITY: city,
                                    Property.NEIGHBORHOOD: neighborhood})
        return response.context['results']


class RecordSearchTest(TestCase):
    def test_existent_record(self):
        """Should return a list with the existent record"""
        prop = mommy.make(Property, num_record=1234)
        response = self.client.get(r('search'),
                                   {Property.RECORD: prop.num_record})
        results = response.context['results']
        self.assertIn(prop, results)

    def test_non_existent_record(self):
        """Should return status 404"""
        response = self.client.get(r('search'),
                                   {Property.RECORD: 555})
        self.assertEqual(404, response.status_code)

    def test_invalid_record(self):
        """Should return status 404"""
        response = self.client.get(r('search'),
                                   {Property.RECORD: 'invalid'})
        self.assertEqual(404, response.status_code)


class SearchPaginationTest(TestCase):
    def test_load_10_properties_per_page(self):
        """Results page must load at maximum 10 properties per page"""
        results = self.get_results(page=1)
        self.assertEqual(10, len(results))

    def test_second_page(self):
        """Results page must load 2 properties on second page"""
        results = self.get_results(page=2)
        self.assertEqual(2, len(results))

    def test_invalid_page(self):
        """Results page must load the first page when param 'pagina' is invalid"""
        results = self.get_results(page='bla')
        self.assertEqual(1, results.number)

    def test_nonexistent_page(self):
        """Results page must load the last page when the page doesn't exist"""
        results = self.get_results(page=10)
        self.assertEqual(2, results.number)

    def get_results(self, page=None):
        create_properties([House],
                          intent=Property.RENT,
                          quantity_each=12)
        response = self.client.get(r('search'), {Property.TYPE: Property.HOUSE,
                                                 Property.INTENT: Property.RENT,
                                                 'pagina': page})
        return response.context['results']


class SearchSortingTest(TestCase):
    def test_sort_by_most_recent(self):
        """Should return properties sorted by most recent"""
        p1, p2, p3, p4 = self.properties_with_prices([Apartment] * 4, [0] * 4)
        expected_order = [p4, p3, p2, p1]

        response = self.client.get(r('search'), {Property.TYPE: Property.APARTMENT,
                                                 Property.INTENT: Property.RENT})
        properties = response.context['properties'].object_list

        self.assertSequenceEqual(expected_order, properties)

    def test_sort_by_lowest_price(self):
        """Should return properties sorted by lowest price"""
        p1, p2, p3, p4 = self.properties_with_prices([Apartment] * 4, [2, 3, 1, 4])
        expected_order = [p3, p1, p2, p4]

        response = self.client.get(r('search'), {Property.TYPE: Property.APARTMENT,
                                                 Property.INTENT: Property.RENT,
                                                 'ordem': 'preco'})
        properties = response.context['properties'].object_list

        self.assertSequenceEqual(expected_order, properties)

    def test_sort_by_highest_price(self):
        """Should return properties sorted by highest price"""
        p1, p2, p3, p4 = self.properties_with_prices([Apartment] * 4, [4, 2, 3, 1])
        expected_order = [p1, p3, p2, p4]

        response = self.client.get(r('search'), {Property.TYPE: Property.APARTMENT,
                                                 Property.INTENT: Property.RENT,
                                                 'ordem': '-preco'})
        properties = response.context['properties'].object_list

        self.assertSequenceEqual(expected_order, properties)

    @staticmethod
    def properties_with_prices(models, prices):
        result = []
        for index, model in enumerate(models):
            result.append(mommy.make(model, intent=Property.RENT, price=prices[index]))
        return result


def create_properties(models, intent, quantity_each):
    for model in models:
        mommy.make(model, intent=intent, _quantity=quantity_each)
    return len(models) * quantity_each
