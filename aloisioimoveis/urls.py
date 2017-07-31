from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from aloisioimoveis.core.redirects import redirect_rent, redirect_buy, redirect_company, redirect_contact, \
    redirect_record, redirect_logo
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
    # Redirects
    url(r'^aluguel.php$', redirect_rent),
    url(r'^venda.php$', redirect_buy),
    url(r'^empresa.php$', redirect_company),
    url(r'^contato.php$', redirect_contact),
    url(r'^ficha.php$', redirect_record),
    url(r'^images/logo.png$', redirect_logo),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
