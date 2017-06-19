from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.properties.models import House, Apartment, Commercial, Land


class PropertyFieldChoicesTest(TestCase):
    def test_has_intent_choices(self):
        """All Property models should have rent and buy choices"""
        models = [
            House,
            Apartment,
            Commercial,
            Land,
        ]
        for model in models:
            self.assertChoicesInField(model, 'intent', ['alugar', 'comprar'])

    def assertChoicesInField(self, model, field_name, choices):
        obj = mommy.make(model)
        field = obj._meta.get_field(field_name)
        for choice in choices:
            with self.subTest():
                self.assertIn(choice, [c[0] for c in field.choices])


class PropertyIsInstanceTest(TestCase):
    def setUp(self):
        self.house = mommy.make(House)
        self.apartment = mommy.make(Apartment)

    def test_is_house(self):
        """Must return True if the property is a House"""
        self.assertTrue(self.house.is_house())

    def test_is_not_house(self):
        """Must return False if the property is not a House"""
        self.assertFalse(self.apartment.is_house())

    def test_is_apartment(self):
        """Must return True if the property is an Apartment"""
        self.assertTrue(self.apartment.is_apartment())

    def test_is_not_apartment(self):
        """Must return False if the property is not an Apartment"""
        self.assertFalse(self.house.is_apartment())
