from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User, Group

from AporteDatabase.models import AporteMes, AporteTotal, HistorialGastos, HistorialPagos

class HistorialPagosAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'comentarios', 'aporte', 'mes', 'ano', )

    search_fields = ('usuario','mes', 'ano', )
    list_filter = ('usuario','mes', 'ano', )


# admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(AporteMes)
admin.site.register(AporteTotal)
admin.site.register(HistorialGastos)
admin.site.register(HistorialPagos, HistorialPagosAdmin)
