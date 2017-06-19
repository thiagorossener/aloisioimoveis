from itertools import chain
from operator import attrgetter

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
    return render(request, 'rent.html')


def buy(request):
    return render(request, 'buy.html')


def search(request):
    return render(request, 'search.html')


def company(request):
    return render(request, 'company.html')


def contact(request):
    return render(request, 'contact.html')
