from itertools import chain
from operator import attrgetter

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render

from aloisioimoveis.properties.models import House, Apartment, Commercial, Land, Property


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
    queries = [model.objects.filter(intent=Property.RENT) for model in models]

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
    queries = (model.objects.filter(intent=Property.BUY) for model in models)

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
    num_record = request.GET.get(Property.RECORD)
    if num_record is not None:
        # Record Number
        try:
            models = [House, Apartment, Commercial, Land]
            queries = [m.objects.filter(num_record=int(num_record)) for m in models]
            queryset = list(chain(*queries))
            if len(queryset) == 0:
                raise Http404('No property matches the record number.')
        except ValueError:
            raise Http404('No property matches the record number.')
    else:
        # Property Type
        property_type = request.GET.get(Property.TYPE)
        if property_type == Property.HOUSE:
            manager = House.objects
        elif property_type == Property.APARTMENT:
            manager = Apartment.objects
        elif property_type == Property.COMMERCIAL:
            manager = Commercial.objects
        elif property_type == Property.LAND:
            manager = Land.objects
        else:
            raise Http404('No property matches the type.')

        # Intent
        intent = request.GET.get(Property.INTENT)
        if intent == Property.RENT:
            queryset = manager.filter(intent=Property.RENT)
        elif intent == Property.BUY:
            queryset = manager.filter(intent=Property.BUY)
        else:
            raise Http404('No property matches the intent.')

        # City
        try:
            city_id = int(request.GET.get(Property.CITY, 0))
        except ValueError:
            city_id = 0
        if city_id > 0:
            queryset = queryset.filter(city__pk=city_id)

        # Neighborhood
        try:
            neighborhood_id = int(request.GET.get(Property.NEIGHBORHOOD, 0))
        except ValueError:
            neighborhood_id = 0
        if neighborhood_id > 0:
            queryset = queryset.filter(neighborhood__pk=neighborhood_id)

    context = {
        'results': list(queryset),
        'params': request.GET.dict(),
    }
    return render(request, 'search.html', context)


def company(request):
    return render(request, 'company.html')


def contact(request):
    return render(request, 'contact.html')
