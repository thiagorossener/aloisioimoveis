from django.contrib import admin

from aloisioimoveis.properties.models import House, Apartment, Commercial, Land


admin.site.register(House)
admin.site.register(Apartment)
admin.site.register(Commercial)
admin.site.register(Land)
