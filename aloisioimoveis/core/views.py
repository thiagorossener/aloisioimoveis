from itertools import chain
from operator import attrgetter

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404

from aloisioimoveis.properties.models import House, Apartment, Commercial, Land


def home(request):
    models = (House, Apartment, Commercial, Land)
    queries = (model.objects.filter(featured=True) for model in models)
    properties = sorted(chain(*queries),
                        key=attrgetter('updated_at'),
                        reverse=True)[:3]
    context = {
        'properties': properties
    }
    return render(request, 'index.html', context)


def rent(request):
    models = (House, Apartment, Commercial, Land)
    queries = [model.objects.filter(intent='alugar') for model in models]

    # Sorting
    sort_key = request.GET.get('ordem')
    if sort_key == 'preco':
        properties_list = sorted(chain(*queries), key=attrgetter('price'))
    elif sort_key == '-preco':
        properties_list = sorted(chain(*queries), key=attrgetter('price'), reverse=True)
    else:
        properties_list = sorted(chain(*queries), key=attrgetter('updated_at'), reverse=True)

    # Pagination
    page = request.GET.get('pagina', 1)
    paginator = Paginator(properties_list, 10)
    try:
        properties = paginator.page(page)
    except PageNotAnInteger:
        properties = paginator.page(1)
    except EmptyPage:
        properties = paginator.page(paginator.num_pages)

    context = {
        'properties': properties,
        'params': request.GET.dict(),
    }
    return render(request, 'rent_list.html', context)


def buy(request):
    # Get all properties
    models = (House, Apartment, Commercial, Land)
    queries = (model.objects.filter(intent='comprar') for model in models)

    # Sorting
    sort_key = request.GET.get('ordem')
    if sort_key == 'preco':
        properties_list = sorted(chain(*queries), key=attrgetter('price'))
    elif sort_key == '-preco':
        properties_list = sorted(chain(*queries), key=attrgetter('price'), reverse=True)
    else:
        properties_list = sorted(chain(*queries), key=attrgetter('updated_at'), reverse=True)

    # Pagination
    page = request.GET.get('pagina', 1)
    paginator = Paginator(properties_list, 10)
    try:
        properties = paginator.page(page)
    except PageNotAnInteger:
        properties = paginator.page(1)
    except EmptyPage:
        properties = paginator.page(paginator.num_pages)

    context = {
        'properties': properties,
        'params': request.GET.dict(),
    }
    return render(request, 'buy_list.html', context)


def search(request):
    return render(request, 'search.html')


def record_house(request, pk):
    prop = get_object_or_404(House, pk=pk)

    # Build field tuples like (col, total, field). Ex: (0, 1, 'bedroom'), (1, 2, 'room')
    total_fields = [f.attname for f in prop._meta.fields if f.attname.startswith('total')]
    prop_dict = model_to_dict(prop)
    fields = []
    for field_name in total_fields:
        if prop_dict[field_name] > 0:
            col = len(fields) % 2
            total = prop_dict[field_name]
            field = field_name.split('total_')[1]
            fields.append((col, total, field))

    context = {
        'property': prop,
        'fields': fields,
        'cols': (0, 1),
    }
    return render(request, 'record.html', context)


def company(request):
    return render(request, 'company.html')


def contact(request):
    return render(request, 'contact.html')
