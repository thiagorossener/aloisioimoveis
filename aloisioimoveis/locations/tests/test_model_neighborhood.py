from datetime import datetime

from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.properties.models import Neighborhood


class NeighborhoodModelTest(TestCase):
    def setUp(self):
        self.obj = mommy.make(Neighborhood)

    def test_create(self):
        """Should create a Neighborhood"""
        self.assertTrue(Neighborhood.objects.exists())

    def test_created_at(self):
        """Neighborhood must have created_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_updated_at(self):
        """Neighborhood must have updated_at attr"""
        self.assertIsInstance(self.obj.updated_at, datetime)

    def test_str(self):
        """str() must return neighborhood name"""
        self.assertEqual(self.obj.name, str(self.obj))
