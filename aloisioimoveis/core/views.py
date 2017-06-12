from django.http import HttpResponse


def home(request):
    return HttpResponse('Site da Imobiliária Aloísio Imóveis no ar')
