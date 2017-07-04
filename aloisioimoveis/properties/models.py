from cloudinary import uploader
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from aloisioimoveis.core.models import BaseModel
from aloisioimoveis.locations.models import City, Neighborhood


class Photo(models.Model):
    content_type = models.ForeignKey('contenttypes.ContentType')
    object_id = models.PositiveIntegerField()
    property = GenericForeignKey()
    image = CloudinaryField('imagem')
    order = models.IntegerField('ordem', default=0)

    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'
        ordering = ['order']

    def __str__(self):
        return 'Foto {}'.format(self.pk)


class Property(BaseModel):
    RECORD = 'ficha'

    TYPE = 'tipo'
    HOUSE = 'casa'
    APARTMENT = 'apartamento'
    COMMERCIAL = 'comercial'
    LAND = 'terreno'

    INTENT = 'finalidade'
    RENT = 'alugar'
    BUY = 'comprar'

    CITY = 'cidade'
    ALL_CITIES = 0

    NEIGHBORHOOD = 'bairro'
    ALL_NEIGHBORHOODS = 0

    INTENT_CHOICES = (
        (RENT, 'Alugar'),
        (BUY, 'Comprar'),
    )

    featured = models.BooleanField('destaque', default=False)
    num_record = models.IntegerField('ficha', null=True, blank=True)
    intent = models.CharField('finalidade', max_length=10, choices=INTENT_CHOICES)
    obs = models.TextField('observações', blank=True)
    price = models.DecimalField('preço', max_digits=11, decimal_places=2)
    conditions = models.CharField('condições', max_length=50, blank=True)
    city = models.ForeignKey(
        City, verbose_name='cidade', related_name='%(app_label)s_%(class)s'
    )
    neighborhood = models.ForeignKey(
        Neighborhood, verbose_name='bairro', related_name='%(app_label)s_%(class)s'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='usuário', related_name='%(app_label)s_%(class)s'
    )
    photos = GenericRelation(Photo)

    def specific(self):
        if hasattr(self, 'house'):
            return self.house
        elif hasattr(self, 'apartment'):
            return self.apartment
        elif hasattr(self, 'commercial'):
            return self.commercial
        elif hasattr(self, 'land'):
            return self.land


class House(Property):
    address = models.CharField('endereço', max_length=200, blank=True)
    total_bedroom = models.IntegerField('dormitórios', default=0)
    total_maids_room = models.IntegerField('dormitórios de empregada', default=0)
    total_maids_wc = models.IntegerField('banheiros de empregada', default=0)
    total_lavatory = models.IntegerField('lavabos', default=0)
    total_room = models.IntegerField('salas', default=0)
    total_kitchen = models.IntegerField('cozinhas', default=0)
    total_hall = models.IntegerField('halls', default=0)
    total_service_area = models.IntegerField('áreas de serviço', default=0)
    total_leisure_area = models.IntegerField('ranchos', default=0)
    total_suite = models.IntegerField('suítes', default=0)
    total_bathroom = models.IntegerField('banheiros', default=0)
    total_coffe_room = models.IntegerField('copas', default=0)
    total_pantry = models.IntegerField('despensas', default=0)
    total_office = models.IntegerField('escritórios', default=0)
    total_garage = models.IntegerField('garagens', default=0)

    @models.permalink
    def get_absolute_url(self):
        return 'records:house', (), {'pk': self.pk}

    def property_type(self):
        return self._meta.verbose_name

    def short_type(self):
        return Property.HOUSE

    class Meta:
        verbose_name = 'Casa'
        verbose_name_plural = 'Casas'

    def __str__(self):
        return 'Casa {} localizada em {}/{}'.format(self.id,
                                                    self.neighborhood,
                                                    self.city)


class Apartment(Property):
    address = models.CharField('endereço', max_length=200, blank=True)
    area = models.CharField('área', max_length=30, blank=True)
    total_bedroom = models.IntegerField('dormitórios', default=0)
    total_maids_room = models.IntegerField('dormitórios de empregada', default=0)
    total_maids_wc = models.IntegerField('banheiros de empregada', default=0)
    total_lavatory = models.IntegerField('lavabos', default=0)
    total_room = models.IntegerField('salas', default=0)
    total_kitchen = models.IntegerField('cozinhas', default=0)
    total_hall = models.IntegerField('halls', default=0)
    total_service_area = models.IntegerField('áreas de serviço', default=0)
    total_suite = models.IntegerField('suítes', default=0)
    total_bathroom = models.IntegerField('banheiros', default=0)
    total_coffe_room = models.IntegerField('copas', default=0)
    total_pantry = models.IntegerField('despensas', default=0)
    total_office = models.IntegerField('escritórios', default=0)
    total_garage = models.IntegerField('garagens', default=0)

    @models.permalink
    def get_absolute_url(self):
        return 'records:apartment', (), {'pk': self.pk}

    def property_type(self):
        return self._meta.verbose_name

    def short_type(self):
        return Property.APARTMENT

    class Meta:
        verbose_name = 'Apartamento'
        verbose_name_plural = 'Apartamentos'

    def __str__(self):
        return 'Apartamento {} localizado em {}/{}'.format(self.id,
                                                           self.neighborhood,
                                                           self.city)


class Commercial(Property):
    address = models.CharField('endereço', max_length=200, blank=True)
    area = models.CharField('área', max_length=30, blank=True)
    total_room = models.IntegerField('salas', default=0)
    total_kitchen = models.IntegerField('cozinhas', default=0)
    total_office = models.IntegerField('escritórios', default=0)
    total_bathroom = models.IntegerField('banheiros', default=0)
    total_garage = models.IntegerField('garagens', default=0)
    total_service_area = models.IntegerField('áreas de serviço', default=0)

    @models.permalink
    def get_absolute_url(self):
        return 'records:commercial', (), {'pk': self.pk}

    def property_type(self):
        return self._meta.verbose_name

    def short_type(self):
        return Property.COMMERCIAL

    class Meta:
        verbose_name = 'Ponto Comercial'
        verbose_name_plural = 'Pontos Comerciais'

    def __str__(self):
        return 'Ponto Comercial {} localizado em {}/{}'.format(self.id,
                                                               self.neighborhood,
                                                               self.city)


class Land(Property):
    address = models.CharField('endereço', max_length=200, blank=True)
    area = models.CharField('área', max_length=30, blank=True)

    @models.permalink
    def get_absolute_url(self):
        return 'records:land', (), {'pk': self.pk}

    def property_type(self):
        return self._meta.verbose_name

    def short_type(self):
        return Property.LAND

    class Meta:
        verbose_name = 'Terreno'
        verbose_name_plural = 'Terrenos'

    def __str__(self):
        return 'Terreno {} localizado em {}/{}'.format(self.id,
                                                       str(self.neighborhood),
                                                       str(self.city))


def post_delete_photo(instance, **kwargs):
    uploader.destroy(instance.image.public_id, invalidate=True)


models.signals.post_delete.connect(
    post_delete_photo, sender=Photo, dispatch_uid='post_delete_photo'
)
