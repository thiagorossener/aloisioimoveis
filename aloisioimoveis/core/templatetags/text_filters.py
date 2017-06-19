from django import template

register = template.Library()


@register.filter
def truncatelinebreaks(value, args="1,100"):
    lines, words = args.split(',')
    result = '\n'.join(list(filter(None, value.splitlines()))[:int(lines)])
    if len(result) < int(words):
        result += '...'
    return result
