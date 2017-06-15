from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from aloisioimoveis.locations.models import City, Neighborhood
from aloisioimoveis.properties.models import House


class HouseModelTest(TestCase):
    def setUp(self):
        city = self.create_city()
        neighborhood = self.create_neighborhood(city=city)
        user = self.create_user()

        self.obj = House(
            featured=True,
            num_record=1234,
            intent='alugar',
            address='Rua Jorge Winther',
            total_bedroom=2,
            total_maids_room=0,
            total_maids_wc=0,
            total_lavatory=0,
            total_room=0,
            total_kitchen=1,
            total_hall=0,
            total_service_area=0,
            total_leisure_area=0,  # rancho
            total_suite=1,
            total_bathroom=2,
            total_coffe_room=0,  # copa
            total_pantry=1,
            total_office=0,
            total_garage=2,
            obs='Tem piscina',
            price=800,
            conditions='IPTU',
            neighborhood=neighborhood,
            city=city,
            user=user,
        )
        self.obj.save()

    def test_create(self):
        """Should create a House"""
        self.assertTrue(House.objects.exists())

    def test_created_at(self):
        """House must have a created_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_updated_at(self):
        """House must have a updated_at attr"""
        self.assertIsInstance(self.obj.updated_at, datetime)

    def create_city(self):
        city = City(
            name='Taubaté'
        )
        city.save()
        return city

    def create_neighborhood(self, city):
        neighborhood = Neighborhood(
            name='Centro',
            city=city
        )
        neighborhood.save()
        return neighborhood

    def create_user(self):
        user = User(
            first_name='Thiago',
            last_name='Rossener',
            email='thiago@rossener.com'
        )
        user.save()
        return user


class HouseFieldChoicesTest(TestCase):
    def setUp(self):
        self.obj = House()

    def test_has_intent_choices(self):
        """Should have rent and buy choices"""
        self.assertChoicesInField('intent', ['alugar', 'comprar'])

    def assertChoicesInField(self, field_name, choices):
        field = self.obj._meta.get_field(field_name)
        for choice in choices:
            with self.subTest():
                self.assertIn(choice, [c[0] for c in field.choices])
