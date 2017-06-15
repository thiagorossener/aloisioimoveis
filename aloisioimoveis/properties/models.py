from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField('nome', max_length=100)

    class Meta:
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    name = models.CharField('nome', max_length=100)
    city = models.ForeignKey(
        City, verbose_name='cidade', related_name='neighborhoods'
    )

    class Meta:
        verbose_name = 'Bairro'
        verbose_name_plural = 'Bairros'

    def __str__(self):
        return self.name


class Property(models.Model):

    INTENT_CHOICES = (
        ('alugar', 'Alugar'),
        ('comprar', 'Comprar'),
    )

    PROPERTY_TYPE_CHOICES = (
        ('casa', 'Casa'),
        ('apartamento', 'Apartamento'),
        ('comercial', 'Comercial'),
        ('terreno', 'Terreno'),
    )

    featured = models.BooleanField('destaque', default=False)
    num_record = models.IntegerField('ficha', null=True)
    intent = models.CharField('finalidade', max_length=10, choices=INTENT_CHOICES)
    property_type = models.CharField('tipo de propriedade', max_length=15, choices=PROPERTY_TYPE_CHOICES)
    address = models.CharField('endereço', max_length=200, blank=True)
    area = models.CharField('área', max_length=30, blank=True)
    in_front_of = models.TextField('em frente a', blank=True)
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
    obs = models.TextField('observações', blank=True)
    price = models.DecimalField('preço', max_digits=11, decimal_places=2)
    conditions = models.CharField('condições', max_length=50, blank=True)
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

    class Meta:
        verbose_name = 'Imóvel'
        verbose_name_plural = 'Imóveis'

    def __str__(self):
        return ' - '.join([self.address, str(self.neighborhood), str(self.city)])
