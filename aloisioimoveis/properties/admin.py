from django.contrib import admin
from django.contrib.contenttypes import admin as generic

from aloisioimoveis.properties.models import House, Apartment, Commercial, Land, Photo


class PhotoInline(generic.GenericTabularInline):
    model = Photo
    extra = 1
    readonly_fields = ['photo_img']
    fields = ['photo_img', 'image', 'order']

    def photo_img(self, obj):
        return '<a href="{0}"><img width="300" src="{0}" /></a>'.format(obj.image.url)

    photo_img.allow_tags = True
    photo_img.short_description = 'foto'


class HouseAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Dados do Registro', {
            'fields': ('featured',
                       'num_record',
                       'intent',
                       ),
        }),
        ('Dados da Localização', {
            'fields': (
                'address',
                'city',
                'neighborhood',
            )
        }),
        ('Dados do Imóvel', {
            'fields': (
                ('total_bedroom', 'total_maids_room', 'total_maids_wc'),
                ('total_lavatory', 'total_room', 'total_kitchen'),
                ('total_hall', 'total_service_area', 'total_leisure_area'),
                ('total_suite', 'total_bathroom', 'total_coffe_room'),
                ('total_pantry', 'total_office', 'total_garage'),
                'obs',
            ),
        }),
        ('Valores', {
            'fields': (
                'price',
                'conditions',
            )
        }),
        ('Auditoria', {
            'fields': ('user',),
        }),
    )
    inlines = [PhotoInline, ]


class ApartmentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Dados do Registro', {
            'fields': ('featured',
                       'num_record',
                       'intent',
                       ),
        }),
        ('Dados da Localização', {
            'fields': (
                'address',
                'city',
                'neighborhood',
            )
        }),
        ('Dados do Imóvel', {
            'fields': (
                'area',
                ('total_bedroom', 'total_maids_room', 'total_maids_wc'),
                ('total_lavatory', 'total_room', 'total_kitchen'),
                ('total_hall', 'total_service_area', 'total_suite'),
                ('total_bathroom', 'total_coffe_room', 'total_pantry'),
                ('total_office', 'total_garage',),
                'obs',
            ),
        }),
        ('Valores', {
            'fields': (
                'price',
                'conditions',
            )
        }),
        ('Auditoria', {
            'fields': ('user',),
        }),
    )
    inlines = [PhotoInline, ]


class CommercialAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Dados do Registro', {
            'fields': ('featured',
                       'num_record',
                       'intent',
                       ),
        }),
        ('Dados da Localização', {
            'fields': (
                'address',
                'city',
                'neighborhood',
            )
        }),
        ('Dados do Imóvel', {
            'fields': (
                'area',
                ('total_room', 'total_kitchen', 'total_office',),
                ('total_bathroom', 'total_garage', 'total_service_area',),
                'obs',
            ),
        }),
        ('Valores', {
            'fields': (
                'price',
                'conditions',
            )
        }),
        ('Auditoria', {
            'fields': ('user',),
        }),
    )
    inlines = [PhotoInline, ]


class LandAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Dados do Registro', {
            'fields': ('featured',
                       'num_record',
                       'intent',
                       ),
        }),
        ('Dados da Localização', {
            'fields': (
                'address',
                'city',
                'neighborhood',
            )
        }),
        ('Dados do Terreno', {
            'fields': (
                'area',
                'obs',
            ),
        }),
        ('Valores', {
            'fields': (
                'price',
                'conditions',
            )
        }),
        ('Auditoria', {
            'fields': ('user',),
        }),
    )
    inlines = [PhotoInline,]


admin.site.register(House, HouseAdmin)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Commercial, CommercialAdmin)
admin.site.register(Land, LandAdmin)
