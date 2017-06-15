from django.contrib import admin

from aloisioimoveis.properties.models import City, Neighborhood, Property


class PropertyAdmin(admin.ModelAdmin):
    fields = (
        'featured',
        'num_record',
        'intent',
        'property_type',
        'address',
        'city',
        'neighborhood',
        ('total_bedroom', 'total_garage', 'total_tv_room'),
        ('total_suite', 'total_kitchen', 'total_service_area'),
        ('total_bathroom', 'total_coffe_room', 'total_leisure_area'),
        ('total_maids_room', 'total_lavatory', 'total_maids_wc'),
        ('total_dining_room', 'total_hall', 'total_living_room'),
        ('total_pantry', 'total_office', 'total_other'),
        'obs',
        'price',
        'conditions',
    )


admin.site.register(Property, PropertyAdmin)
admin.site.register(Neighborhood)
admin.site.register(City)
