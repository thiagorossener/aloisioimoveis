from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from aloisioimoveis.core.views import home, rent, buy, search, contact, company

urlpatterns = [
    # Views
    url(r'^$', home, name='home'),
    url(r'^alugar/$', rent, name='rent'),
    url(r'^comprar/$', buy, name='buy'),
    url(r'^buscar/$', search, name='search'),
    url(r'^imovel/', include('aloisioimoveis.properties.urls', namespace='records')),
    url(r'^empresa/$', company, name='company'),
    url(r'^contato/$', contact, name='contact'),
    url(r'^sistema/', admin.site.urls),
    # API
    url(r'^api/locations/', include('aloisioimoveis.locations.urls', namespace='locations')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
