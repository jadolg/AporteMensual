from __future__ import unicode_literals
from django.utils.six import python_2_unicode_compatible
from django.db import models


# Create your models here.

@python_2_unicode_compatible
class AporteMes(models.Model):
    usuario = models.CharField(max_length=100)
    comentarios = models.CharField(max_length=1000, null=True)
    rango = models.CharField(max_length=100)
    cant_usuarios = models.IntegerField(default=0)
    aporte = models.FloatField(default=0)

    def __str__(self):
        return self.usuario


@python_2_unicode_compatible
class AporteTotal(models.Model):
    aporte = models.FloatField(default=0)

    def __str__(self):
        return str(self.aporte)


@python_2_unicode_compatible
class HistorialGastos(models.Model):
    cantidad = models.FloatField(default=0)
    comentarios = models.CharField(max_length=1000, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.cantidad) + "  " + self.motivo


@python_2_unicode_compatible
class HistorialPagos(models.Model):
    usuario = models.CharField(max_length=100)
    comentarios = models.CharField(max_length=1000)
    aporte = models.FloatField(default=0)
    mes = models.IntegerField(default=0)
    ano = models.IntegerField(default=0)
    # fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.aporte) + "  " + self.usuario