from django.test import TestCase

from aloisioimoveis.core.templatetags import text_filters


class TextFiltersTest(TestCase):
    def test_truncatelinebreaks_one_br(self):
        """Given a line with 1 linebreak, truncate before"""
        text = 'Este é um texto com\numa quebra de linha'
        self.assertEqual('Este é um texto com...', text_filters.truncatelinebreaks(text))

    def test_truncatelinebreaks_no_br(self):
        """Given a line without linebreaks, no truncate"""
        text = 'Este é um texto sem quebra de linha'
        self.assertEqual(text + '...', text_filters.truncatelinebreaks(text))

    def test_truncatelinebreaks_many_brs(self):
        """Given a line with many linebreaks, truncate before given number"""
        text = 'Esta é\n\numa linha\n\n\ncom várias\nquebras de\nlinha'
        self.assertEqual('Esta é\numa linha\ncom várias...',
                         text_filters.truncatelinebreaks(text, '3,100'))
