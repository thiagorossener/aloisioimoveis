from datetime import datetime

from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.properties.models import Apartment


class ApartmentModelTest(TestCase):
    def setUp(self):
        self.obj = mommy.make(Apartment)

    def test_create(self):
        """Should create an Apartment"""
        self.assertTrue(Apartment.objects.exists())

    def test_created_at(self):
        """Apartment must have a created_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_updated_at(self):
        """Apartment must have a updated_at attr"""
        self.assertIsInstance(self.obj.updated_at, datetime)

    def test_str(self):
        """str() must return 'Apartamento [id] localizado em [Neightbodhood]/[City]"""
        self.assertEqual('Apartamento {} localizado em {}/{}'
                         .format(self.obj.id, self.obj.neighborhood, self.obj.city),
                         str(self.obj))

    def test_property_type(self):
        """property_type() must return 'Apartamento'"""
        self.assertEqual('Apartamento', self.obj.property_type())
