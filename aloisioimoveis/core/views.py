from itertools import chain
from operator import attrgetter

from django.shortcuts import render

from aloisioimoveis.properties.models import House, Apartment, Commercial, Land


def home(request):
    query1 = list(House.objects.filter(featured=True))
    query2 = list(Apartment.objects.filter(featured=True))
    query3 = list(Commercial.objects.filter(featured=True))
    query4 = list(Land.objects.filter(featured=True))
    properties = sorted(
        chain(query1, query2, query3, query4),
        key=attrgetter('updated_at'),
        reverse=True
    )[:3]
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
