from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from aloisioimoveis.properties.models import City, Neighborhood, Apartment


class ApartmentModelTest(TestCase):
    def setUp(self):
        city = self.create_city()
        neighborhood = self.create_neighborhood(city=city)
        user = self.create_user()

        self.obj = Apartment(
            featured=True,
            num_record=1234,
            intent='comprar',
            address='Rua Jorge Winther',
            total_bedroom=2,
            total_maids_room=0,
            total_maids_wc=0,
            total_lavatory=0,
            total_dining_room=0,
            total_kitchen=1,
            total_hall=0,
            total_service_area=0,
            total_leisure_area=0,  # rancho
            total_suite=1,
            total_bathroom=2,
            total_living_room=1,
            total_tv_room=1,
            total_coffe_room=0,  # copa
            total_pantry=1,
            total_office=0,
            total_garage=2,
            total_other=0,
            obs='Tem piscina',
            price=800,
            conditions='IPTU',
            neighborhood=neighborhood,
            city=city,
            user=user,
        )
        self.obj.save()

    def test_create(self):
        """Should create an Apartment"""
        self.assertTrue(Apartment.objects.exists())

    def test_created_at(self):
        """Apartment must have a created_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_updated_at(self):
        """Apartment must have a updated_at attr"""
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


class ApartmentFieldChoicesTest(TestCase):
    def setUp(self):
        self.obj = Apartment()

    def test_has_intent_choices(self):
        """Should have rent and buy choices"""
        self.assertChoicesInField('intent', ['alugar', 'comprar'])

    def assertChoicesInField(self, field_name, choices):
        field = self.obj._meta.get_field(field_name)
        for choice in choices:
            with self.subTest():
                self.assertIn(choice, [c[0] for c in field.choices])
