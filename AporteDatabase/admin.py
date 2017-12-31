from django.contrib import admin
from django.contrib.auth.models import Group

from AporteDatabase.models import Identidad


class IdentidadAdmin(admin.ModelAdmin):
    list_display = ('nombre_nodo', 'logo_nodo', 'hint_rango', 'en_uso')


admin.site.unregister(Group)
admin.site.register(Identidad, IdentidadAdmin)
