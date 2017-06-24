from django.http import JsonResponse, HttpResponseServerError

from aloisioimoveis.locations.models import City, Neighborhood
from aloisioimoveis.locations.serializers import CitySerializer, NeighborhoodSerializer


def cities(request):
    all_cities = City.objects.all()
    serializer = CitySerializer(all_cities, many=True)
    return JsonResponse(serializer.data, safe=False)


def neighborhoods(request):
    try:
        all_neighborhoods = Neighborhood.objects.filter(city__pk=request.GET.get('city'))
    except ValueError:
        return HttpResponseServerError()
    serializer = NeighborhoodSerializer(all_neighborhoods, many=True)
    return JsonResponse(serializer.data, safe=False)

