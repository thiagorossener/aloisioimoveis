from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def rent(request):
    return render(request, 'rent.html')
