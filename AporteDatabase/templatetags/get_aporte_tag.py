from datetime import date
from django import template

from AporteDatabase.models import AporteTotal, AporteMes, HistorialPagos

register = template.Library()


@register.simple_tag
def get_aporte():
    try:
        return AporteTotal.objects.all()[0].aporte
    except:
        AporteTotal(aporte=0).save()
        return AporteTotal.objects.all()[0].aporte


@register.simple_tag
def get_aporte_mes():
    totalmes = 0
    for i in HistorialPagos.objects.filter(mes=date.today().month, ano=date.today().year):
        totalmes += i.aporte
    return totalmes
