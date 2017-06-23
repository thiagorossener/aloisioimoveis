from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from aloisioimoveis.core.views import home, rent, buy, search, contact, company, record_house, record_apartment, \
    record_commercial, record_land

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^alugar/$', rent, name='rent'),
    url(r'^comprar/$', buy, name='buy'),
    url(r'^buscar/$', search, name='search'),
    url(r'^imovel/casa/(?P<pk>\d+)/$', record_house, name='record_house'),
    url(r'^imovel/apartamento/(?P<pk>\d+)/$', record_apartment, name='record_apartment'),
    url(r'^imovel/comercial/(?P<pk>\d+)/$', record_commercial, name='record_commercial'),
    url(r'^imovel/terreno/(?P<pk>\d+)/$', record_land, name='record_land'),
    url(r'^empresa/$', company, name='company'),
    url(r'^contato/$', contact, name='contact'),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
