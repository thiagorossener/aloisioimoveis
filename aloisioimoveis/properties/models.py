from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from aloisioimoveis.core.models import BaseModel
from aloisioimoveis.locations.models import City, Neighborhood


class Photo(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    property = GenericForeignKey()
    image = CloudinaryField('imagem')
    order = models.IntegerField('ordem', default=0)

    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'
        ordering = ['order']

    def __str__(self):
        return str(self.image)


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
        User, verbose_name='usuário', related_name='%(app_label)s_%(class)s'
    )
    photos = GenericRelation(Photo)

    class Meta:
        abstract = True

    def property_type(self):
        return self._meta.verbose_name

    def is_house(self):
        return isinstance(self, House)

    def is_apartment(self):
        return isinstance(self, Apartment)


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
        return 'records:house', (), { 'pk': self.pk }

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

    class Meta:
        verbose_name = 'Terreno'
        verbose_name_plural = 'Terrenos'

    def __str__(self):
        return 'Terreno {} localizado em {}/{}'.format(self.id,
                                                       str(self.neighborhood),
                                                       str(self.city))
