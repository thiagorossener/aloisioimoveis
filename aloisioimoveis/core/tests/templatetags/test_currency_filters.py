from django.test import TestCase

from aloisioimoveis.core.templatetags import currency_filters


class CurrencyFiltersTest(TestCase):
    def test_currency_brl(self):
        """For the input 1000, should return output R$ 1.000,00"""
        self.assertEqual('R$ 1.000,00', currency_filters.currency_brl(1000))
