"""AporteMensual URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin


from AporteDatabase.views import index, login_user, logout_user, add_user, delete_user, pagar, restart, gastos, undo, \
    historial_aporte, subsanar_gasto

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^login$', login_user, name='login'),
    url(r'^logout$', logout_user, name='logout'),
    url(r'^adduser$', add_user, name='add_user'),
    url(r'^delete/(?P<uid>[0-9]+)$', delete_user, name='delete_user'),
    url(r'^undo/(?P<uid>[0-9]+)$', undo, name='undo'),
    url(r'^pagar/(?P<uid>[0-9]+)$', pagar, name='pagar'),
    url(r'^pagar$', pagar, name='pagar'),
    url(r'^restart$', restart, name='restart'),
    url(r'^gastos$', gastos, name='gastos'),
    url(r'^historial$', historial_aporte, name='historial_aporte'),
    url(r'^historial/(?P<year>[0-9]+)$', historial_aporte, name='historial_aporte'),
    url(r'^subsanar_gasto/(?P<id>[0-9]+)', subsanar_gasto, name='subsanar_gasto'),
]
