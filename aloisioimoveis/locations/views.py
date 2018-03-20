from dal import autocomplete
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


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return City.objects.none()

        qs = City.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class NeighborhoodAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Neighborhood.objects.none()

        qs = Neighborhood.objects.all()

        city = self.forwarded.get('city', None)

        if city:
            qs = qs.filter(city=city)

            if self.q:
                qs = qs.filter(name__istartswith=self.q)

            return qs

        return Neighborhood.objects.none()
