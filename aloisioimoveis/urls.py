from django.conf.urls import url
from django.contrib import admin

from aloisioimoveis.core.views import home

urlpatterns = [
    url(r'^$', home),
    url(r'^admin/', admin.site.urls),
]
