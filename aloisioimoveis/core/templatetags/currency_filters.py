from django import template

register = template.Library()


@register.filter
def currency_brl(value):
    return 'R$ {:,.2f}'.format(value).replace(',', 'X').replace('.', ',').replace('X', '.')
