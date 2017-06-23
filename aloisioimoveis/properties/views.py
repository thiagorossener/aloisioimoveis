from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render

from aloisioimoveis.properties.models import House, Apartment, Commercial, Land


def house(request, pk):
    prop = get_object_or_404(House, pk=pk)
    fields = _build_total_field_tuples(prop)
    context = {
        'property': prop,
        'fields': fields,
        'cols': (0, 1),
    }
    return render(request, 'record.html', context)


def apartment(request, pk):
    prop = get_object_or_404(Apartment, pk=pk)
    fields = _build_total_field_tuples(prop)
    context = {
        'property': prop,
        'fields': fields,
        'cols': (0, 1),
    }
    return render(request, 'record.html', context)


def commercial(request, pk):
    prop = get_object_or_404(Commercial, pk=pk)
    fields = _build_total_field_tuples(prop)
    context = {
        'property': prop,
        'fields': fields,
        'cols': (0, 1),
    }
    return render(request, 'record.html', context)


def land(request, pk):
    prop = get_object_or_404(Land, pk=pk)
    context = {
        'property': prop,
    }
    return render(request, 'record.html', context)


def _build_total_field_tuples(obj):
    # Build field tuples like (col, total, field). Ex: (0, 1, 'bedroom'), (1, 2, 'room')
    total_fields = [f.attname for f in obj._meta.fields if f.attname.startswith('total')]
    prop_dict = model_to_dict(obj)
    fields = []
    for field_name in total_fields:
        if prop_dict[field_name] > 0:
            col = len(fields) % 2
            total = prop_dict[field_name]
            field = field_name.split('total_')[1]
            fields.append((col, total, field))
    return fields
