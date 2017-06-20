from collections import OrderedDict
from urllib.parse import urlencode

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(OrderedDict(sorted(query.items())))
