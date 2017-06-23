from django.conf.urls import url

from aloisioimoveis.properties.views import house, apartment, commercial, land

urlpatterns = [
    url(r'^casa/(?P<pk>\d+)/$', house, name='house'),
    url(r'^apartamento/(?P<pk>\d+)/$', apartment, name='apartment'),
    url(r'^comercial/(?P<pk>\d+)/$', commercial, name='commercial'),
    url(r'^terreno/(?P<pk>\d+)/$', land, name='land'),
]
