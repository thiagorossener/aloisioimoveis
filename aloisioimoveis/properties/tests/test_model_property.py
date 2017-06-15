from datetime import datetime

from django.test import TestCase

from aloisioimoveis.properties.models import Property, Neighborhood, City, User


class PropertyModelTest(TestCase):
    def setUp(self):
        city = self.create_city()
        neighborhood = self.create_neighborhood(city=city)
        user = self.create_user()

        self.obj = Property(
            featured=True,
            num_record=1234,
            intent='alugar',
            property_type='casa',
            address='Rua Jorge Winther',
            area='120m2',
            in_front_of='Cool Street',
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
        """Should create a Property"""
        self.assertTrue(Property.objects.exists())

    def test_user(self):
        """Property must have a User attr"""
        self.assertIsInstance(self.obj.user, User)

    def test_city(self):
        """Property must have a City attr"""
        self.assertIsInstance(self.obj.city, City)

    def test_neighborhood(self):
        """Property must have a Neighborhood attr"""
        self.assertIsInstance(self.obj.neighborhood, Neighborhood)

    def test_created_at(self):
        """Property must have a created_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_updated_at(self):
        """Property must have a updated_at attr"""
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


class PropertyFieldChoicesTest(TestCase):
    def setUp(self):
        self.obj = Property()

    def test_has_intent_choices(self):
        """Should have rent and buy choices"""
        self.assertChoicesInField('intent', ['alugar', 'comprar'])

    def test_has_property_type_choices(self):
        """Should have property types house, apartment, comercial and terrain"""
        self.assertChoicesInField('property_type', ['casa', 'apartamento', 'comercial', 'terreno'])

    def assertChoicesInField(self, field_name, choices):
        field = self.obj._meta.get_field(field_name)
        for choice in choices:
            with self.subTest():
                self.assertIn(choice, [c[0] for c in field.choices])
