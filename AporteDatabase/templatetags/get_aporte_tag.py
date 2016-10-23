from django import template

from AporteDatabase.models import AporteTotal, AporteMes

register = template.Library()


@register.simple_tag
def get_aporte():
    return AporteTotal.objects.all()[0].aporte


@register.simple_tag
def get_aporte_mes():
    totalmes = 0
    for i in AporteMes.objects.all():
        totalmes += i.aporte
    return totalmes
