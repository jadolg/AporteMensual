from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.six import python_2_unicode_compatible
from django.db import models


# Create your models here.
from AporteMensual.settings import MEDIA_ROOT


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
    motivo = models.CharField(max_length=10000)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.cantidad) + "  " + self.motivo


@python_2_unicode_compatible
class HistorialPagos(models.Model):
    usuario = models.CharField(max_length=100)
    comentarios = models.CharField(max_length=1000, null=True)
    aporte = models.FloatField(default=0)
    mes = models.IntegerField(default=0)
    ano = models.IntegerField(default=0)
    # fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.aporte) + "  " + self.usuario


@python_2_unicode_compatible
class Identidad(models.Model):
    nombre_nodo = models.CharField(max_length=100)
    logo_nodo = models.FileField(upload_to=MEDIA_ROOT)
    en_uso = models.BooleanField(default=False)
    hint_rango = models.CharField(max_length=15)


@receiver(post_save, sender=Identidad)
def create_identidad(sender, instance, created, **kwargs):
    if instance.en_uso:
        for identidad in Identidad.objects.all():
            if identidad != instance:
                identidad.en_uso = False
                identidad.save()
