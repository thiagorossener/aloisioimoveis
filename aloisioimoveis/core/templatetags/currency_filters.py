import locale

from django import template

register = template.Library()


@register.filter
def currency_brl(value):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    return 'R$ {}'.format(locale.currency(value, grouping=True, symbol=None))
