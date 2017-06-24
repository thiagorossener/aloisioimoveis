from django.conf.urls import url

from aloisioimoveis.locations.views import cities, neighborhoods


urlpatterns = [
    url(r'^cities', cities, name='cities'),
    url(r'^neighborhoods', neighborhoods, name='neighborhoods'),
]
