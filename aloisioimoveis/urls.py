from django.conf.urls import url
from django.contrib import admin

from aloisioimoveis.core.views import home, rent

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^alugar/$', rent, name='rent'),
    url(r'^admin/', admin.site.urls),
]
