from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField('nome', max_length=100)


class Neighborhood(models.Model):
    name = models.CharField('nome', max_length=100)
    city = models.ForeignKey(
        City, verbose_name='cidade', related_name='neighborhoods'
    )


class Property(models.Model):
    featured = models.BooleanField('destaque', default=False)
    intent = models.CharField('finalidade', max_length=10)
    property_type = models.CharField('tipo de propriedade', max_length=15)
    address = models.CharField('endereço', max_length=200)
    area = models.CharField('área', max_length=30)
    in_front_of = models.TextField('em frente a')
    total_bedroom = models.IntegerField('dormitórios')
    total_maids_room = models.IntegerField('dormitórios de empregada')
    total_maids_wc = models.IntegerField('banheiros de empregada')
    total_lavatory = models.IntegerField('lavabos')
    total_dining_room = models.IntegerField('salas de refeição')
    total_kitchen = models.IntegerField('cozinhas')
    total_hall = models.IntegerField('halls')
    total_service_area = models.IntegerField('áreas de serviço')
    total_leisure_area = models.IntegerField('ranchos')
    total_suite = models.IntegerField('suítes')
    total_bathroom = models.IntegerField('banheiros')
    total_living_room = models.IntegerField('salas de estar')
    total_tv_room = models.IntegerField('salas de tv')
    total_coffe_room = models.IntegerField('copas')
    total_pantry = models.IntegerField('despensas')
    total_office = models.IntegerField('escritórios')
    total_garage = models.IntegerField('garagens')
    total_other = models.IntegerField('outros')
    obs = models.TextField('observações')
    price = models.DecimalField('preço', max_digits=11, decimal_places=2)
    conditions = models.CharField('condições', max_length=50)
    city = models.ForeignKey(
        City, verbose_name='cidade', related_name='properties'
    )
    neighborhood = models.ForeignKey(
        Neighborhood, verbose_name='bairro', related_name='properties'
    )
    user = models.ForeignKey(
        User, verbose_name='usuário', related_name='properties'
    )
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)
