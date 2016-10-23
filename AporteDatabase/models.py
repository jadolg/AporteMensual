from __future__ import unicode_literals

from django.db import models

# Create your models here.

class AporteMes(models.Model):
    usuario = models.CharField(max_length=100)
    aporte =  models.FloatField(default=0)

    def __str__(self):
        return self.usuario

class AporteTotal(models.Model):
    aporte = models.FloatField(default=0)

    def __str__(self):
        return self.aporte

class HistorialGastos(models.Model):
    cantidad = models.FloatField(default=0)
    motivo = models.CharField(max_length=10000)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.cantidad)+"  "+self.motivo