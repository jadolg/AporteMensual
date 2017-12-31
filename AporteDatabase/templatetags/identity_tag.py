from django import template

from AporteDatabase.models import Identidad

register = template.Library()


@register.simple_tag
def get_identity_name():
    en_uso = Identidad.objects.filter(en_uso=True)
    if len(en_uso) > 0:
        return en_uso[0].nombre_nodo
    else:
        return 'SIN NOMBRE'


@register.simple_tag
def get_identity_image():
    en_uso = Identidad.objects.filter(en_uso=True)
    if len(en_uso) > 0:
        return en_uso[0].logo_nodo.url
    else:
        return '.'


@register.simple_tag
def get_identity_rango():
    en_uso = Identidad.objects.filter(en_uso=True)
    if len(en_uso) > 0:
        return en_uso[0].hint_rango
    else:
        return '0.0.0.0'
