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
