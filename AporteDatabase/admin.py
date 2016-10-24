from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User, Group

from AporteDatabase.models import AporteMes, AporteTotal, HistorialGastos, HistorialPagos

# admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(AporteMes)
admin.site.register(AporteTotal)
admin.site.register(HistorialGastos)
admin.site.register(HistorialPagos)
