from django.conf.urls import url
from django.contrib import admin

from aloisioimoveis.core.views import home, rent

urlpatterns = [
    url(r'^$', home),
    url(r'^alugar/$', rent),
    url(r'^admin/', admin.site.urls),
]
