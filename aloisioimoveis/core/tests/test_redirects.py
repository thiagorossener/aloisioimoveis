from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.properties.models import House, Apartment, Commercial, Land


class RedirectTests(TestCase):
    def test_rent_redirect(self):
        """GET /aluguel.php should redirect to /alugar/"""
        response = self.client.get('/aluguel.php')
        self.assertRedirects(response, r('rent'), 301)

    def test_buy_redirect(self):
        """GET /venda.php should redirect to /comprar/"""
        response = self.client.get('/venda.php')
        self.assertRedirects(response, r('buy'), 301)

    def test_company_redirect(self):
        """GET /empresa.php should redirect to /empresa/"""
        response = self.client.get('/empresa.php')
        self.assertRedirects(response, r('company'), 301)

    def test_contact_redirect(self):
        """GET /contato.php should redirect to /contato/"""
        response = self.client.get('/contato.php')
        self.assertRedirects(response, r('contact'), 301)

    def test_record_redirect(self):
        """GET /ficha.php should return 404 status code"""
        response = self.client.get('/ficha.php')
        self.assertEqual(404, response.status_code)

    def test_record_invalid_redirect(self):
        """GET /ficha.php?id=bla should return 404 status code"""
        response = self.client.get('/ficha.php?id=bla')
        self.assertEqual(404, response.status_code)

    def test_record_nonexistent_redirect(self):
        """GET /ficha.php?id=999 should return 404 status code"""
        response = self.client.get('/ficha.php?id=999')
        self.assertEqual(404, response.status_code)

    def test_record_house_redirect(self):
        """GET /ficha.php?id=1 should redirect to /imovel/casa/1/"""
        prop = mommy.make(House)
        response = self.client.get('/ficha.php?id=1')
        self.assertRedirects(response, r('records:house', pk=prop.pk), 301)

    def test_record_apartment_redirect(self):
        """GET /ficha.php?id=1 should redirect to /imovel/apartamento/1/"""
        prop = mommy.make(Apartment)
        response = self.client.get('/ficha.php?id=1')
        self.assertRedirects(response, r('records:apartment', pk=prop.pk), 301)

    def test_record_commercial_redirect(self):
        """GET /ficha.php?id=1 should redirect to /imovel/comercial/1/"""
        prop = mommy.make(Commercial)
        response = self.client.get('/ficha.php?id=1')
        self.assertRedirects(response, r('records:commercial', pk=prop.pk), 301)

    def test_record_land_redirect(self):
        """GET /ficha.php?id=1 should redirect to /imovel/terreno/1/"""
        prop = mommy.make(Land)
        response = self.client.get('/ficha.php?id=1')
        self.assertRedirects(response, r('records:land', pk=prop.pk), 301)
