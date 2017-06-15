from django.contrib import admin

from aloisioimoveis.properties.models import City, Neighborhood, House, Apartment, Commercial, Land


admin.site.register(House)
admin.site.register(Apartment)
admin.site.register(Commercial)
admin.site.register(Land)
admin.site.register(Neighborhood)
admin.site.register(City)
