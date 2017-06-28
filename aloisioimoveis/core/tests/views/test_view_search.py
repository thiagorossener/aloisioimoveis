from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy

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
        house = mommy.make(House, num_record=1234)
        response = self.client.get(r('search'),
                                   {Property.RECORD: house.num_record})
        results = response.context['results']
        self.assertIn(house, results)

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
