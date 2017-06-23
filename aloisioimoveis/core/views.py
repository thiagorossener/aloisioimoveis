from itertools import chain
from operator import attrgetter

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

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


def company(request):
    return render(request, 'company.html')


def contact(request):
    return render(request, 'contact.html')
