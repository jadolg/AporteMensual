from django.contrib import admin
from django.contrib.auth.models import Group

from AporteDatabase.models import Identidad, HistorialPagos


class HistorialPagosAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'comentarios', 'aporte', 'mes', 'ano',)

    search_fields = ('usuario', 'mes', 'ano',)
    list_filter = ('usuario', 'mes', 'ano',)


class IdentidadAdmin(admin.ModelAdmin):
    list_display = ('nombre_nodo', 'logo_nodo', 'hint_rango', 'en_uso')


admin.site.unregister(Group)
admin.site.register(Identidad, IdentidadAdmin)
admin.site.register(HistorialPagos, HistorialPagosAdmin)
