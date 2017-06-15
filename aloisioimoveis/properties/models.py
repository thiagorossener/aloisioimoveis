from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from aloisioimoveis.core.models import BaseModel
from aloisioimoveis.locations.models import City, Neighborhood


class Property(BaseModel):

    INTENT_CHOICES = (
        ('alugar', 'Alugar'),
        ('comprar', 'Comprar'),
    )

    featured = models.BooleanField('destaque', default=False)
    num_record = models.IntegerField('ficha', null=True)
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

    class Meta:
        abstract = True


class House(Property):
    address = models.CharField('endereço', max_length=200, blank=True)
    total_bedroom = models.IntegerField('dormitórios', default=0)
    total_maids_room = models.IntegerField('dormitórios de empregada', default=0)
    total_maids_wc = models.IntegerField('banheiros de empregada', default=0)
    total_lavatory = models.IntegerField('lavabos', default=0)
    total_dining_room = models.IntegerField('salas de refeição', default=0)
    total_kitchen = models.IntegerField('cozinhas', default=0)
    total_hall = models.IntegerField('halls', default=0)
    total_service_area = models.IntegerField('áreas de serviço', default=0)
    total_leisure_area = models.IntegerField('ranchos', default=0)
    total_suite = models.IntegerField('suítes', default=0)
    total_bathroom = models.IntegerField('banheiros', default=0)
    total_living_room = models.IntegerField('salas de estar', default=0)
    total_tv_room = models.IntegerField('salas de tv', default=0)
    total_coffe_room = models.IntegerField('copas', default=0)
    total_pantry = models.IntegerField('despensas', default=0)
    total_office = models.IntegerField('escritórios', default=0)
    total_garage = models.IntegerField('garagens', default=0)
    total_other = models.IntegerField('outros', default=0)

    class Meta:
        verbose_name = 'Casa'
        verbose_name_plural = 'Casas'


class Apartment(Property):
    address = models.CharField('endereço', max_length=200, blank=True)
    total_bedroom = models.IntegerField('dormitórios', default=0)
    total_maids_room = models.IntegerField('dormitórios de empregada', default=0)
    total_maids_wc = models.IntegerField('banheiros de empregada', default=0)
    total_lavatory = models.IntegerField('lavabos', default=0)
    total_dining_room = models.IntegerField('salas de refeição', default=0)
    total_kitchen = models.IntegerField('cozinhas', default=0)
    total_hall = models.IntegerField('halls', default=0)
    total_service_area = models.IntegerField('áreas de serviço', default=0)
    total_leisure_area = models.IntegerField('ranchos', default=0)
    total_suite = models.IntegerField('suítes', default=0)
    total_bathroom = models.IntegerField('banheiros', default=0)
    total_living_room = models.IntegerField('salas de estar', default=0)
    total_tv_room = models.IntegerField('salas de tv', default=0)
    total_coffe_room = models.IntegerField('copas', default=0)
    total_pantry = models.IntegerField('despensas', default=0)
    total_office = models.IntegerField('escritórios', default=0)
    total_garage = models.IntegerField('garagens', default=0)
    total_other = models.IntegerField('outros', default=0)

    class Meta:
        verbose_name = 'Apartamento'
        verbose_name_plural = 'Apartamentos'


class Commercial(Property):
    address = models.CharField('endereço', max_length=200, blank=True)
    area = models.CharField('área', max_length=30, blank=True)
    obs = models.TextField('observações', blank=True)
    price = models.DecimalField('preço', max_digits=11, decimal_places=2)
    conditions = models.CharField('condições', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Ponto Comercial'
        verbose_name_plural = 'Pontos Comerciais'


class Land(Property):
    area = models.CharField('área', max_length=30, blank=True)
    in_front_of = models.TextField('em frente a', blank=True)

    class Meta:
        verbose_name = 'Terreno'
        verbose_name_plural = 'Terrenos'
