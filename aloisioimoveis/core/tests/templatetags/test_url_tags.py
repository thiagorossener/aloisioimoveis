from django.http import QueryDict
from django.template import Context
from django.test import TestCase, RequestFactory

from aloisioimoveis.core.templatetags import url_tags


class UrlReplaceTagTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_replace_one_param(self):
        """Should replace a simple param"""
        context = self.create_context_with('pagina=1')
        self.assertEqual(QueryDict('pagina=2'),
                         QueryDict(url_tags.url_replace(context, pagina=2)))

    def test_replace_many_params(self):
        """Should replace many params"""
        context = self.create_context_with('pagina=1&ordem=preco')
        self.assertEqual(QueryDict('pagina=2&ordem=-preco'),
                         QueryDict(url_tags.url_replace(context, pagina=2, ordem='-preco')))

    def test_replace_some_params(self):
        """Should replace some params"""
        context = self.create_context_with('pagina=1&ordem=preco&ficha=10')
        self.assertEqual(QueryDict('pagina=2&ordem=preco&ficha=11'),
                         QueryDict(url_tags.url_replace(context, pagina=2, ficha=11)))

    def create_context_with(self, params):
        request = self.factory.get('?' + params)
        return Context({'request': request})
