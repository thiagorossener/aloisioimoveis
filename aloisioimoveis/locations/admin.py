from django.contrib import admin

from aloisioimoveis.locations.models import Neighborhood, City


class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'city_name')

    def city_name(self, obj):
        return obj.city.name

    city_name.short_description = 'cidade'
    city_name.admin_order_field = 'city__name'

admin.site.register(Neighborhood, NeighborhoodAdmin)
admin.site.register(City)
