from django.conf.urls import url
from django.contrib import admin

from aloisioimoveis.core.views import home, rent, buy, search, contact

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^alugar/$', rent, name='rent'),
    url(r'^comprar/$', buy, name='buy'),
    url(r'^buscar/$', search, name='search'),
    url(r'^contato/$', contact, name='contact'),
    url(r'^admin/', admin.site.urls),
]
