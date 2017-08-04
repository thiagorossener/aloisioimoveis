from django.db import models

from aloisioimoveis.core.models import BaseModel


class City(BaseModel):
    name = models.CharField('nome', max_length=100)

    class Meta:
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'
        ordering = ['name']

    def __str__(self):
        return self.name


class Neighborhood(BaseModel):
    name = models.CharField('nome', max_length=100)
    city = models.ForeignKey(
        City, verbose_name='cidade', related_name='neighborhoods'
    )

    class Meta:
        verbose_name = 'Bairro'
        verbose_name_plural = 'Bairros'
        ordering = ['name']

    def __str__(self):
        return self.name
