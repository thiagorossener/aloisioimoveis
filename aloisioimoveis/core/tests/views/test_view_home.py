from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.properties.models import House, Apartment, Commercial, Land, Property


class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('home'))

    def test_get(self):
        """GET / should return status 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, 'index.html')


class HomeContextTest(TestCase):
    def setUp(self):
        self.models = self.create_properties([House,
                                              Apartment,
                                              Commercial,
                                              Land])
        response = self.client.get(r('home'))
        self.properties = response.context['properties']

    def test_context_min_properties(self):
        """Home must load at minimum 1 property"""
        self.assertTrue(len(self.properties) > 0)

    def test_context_max_properties(self):
        """Home must load at maximum 3 properties"""
        self.assertTrue(len(self.properties) <= 3)

    def test_context_all_property_types(self):
        """Home must load only property types"""
        for prop in self.properties:
            with self.subTest():
                self.assertIsInstance(prop, Property)

    def test_context_featured_properties(self):
        """Home must load the last 3 featured properties"""
        self.assertEqual(self.properties[0].specific(), self.models[3])
        self.assertEqual(self.properties[1].specific(), self.models[2])
        self.assertEqual(self.properties[2].specific(), self.models[1])

    @staticmethod
    def create_properties(models):
        return [mommy.make(m, featured=True) for m in models]
