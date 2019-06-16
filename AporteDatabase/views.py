from datetime import datetime, date

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from AporteDatabase.models import Usuario, AporteTotal, HistorialGastos, HistorialPagos
from django.contrib import messages


def index(request):
    # pagado = AporteMes.objects.filter(aporte__gt=0)
    pagado = HistorialPagos.objects.filter(mes=date.today().month, ano=date.today().year)
    nombres_pagados = []
    total_mes = 0.0
    for i in pagado:
        nombres_pagados.append(i.usuario)
        total_mes += i.aporte

    nopagado = []
    for i in Usuario.objects.all():
        if i.usuario not in nombres_pagados:
            nopagado.append(i)

    return render(request, "index.html", {"total_mes": total_mes, "aportes": pagado, "noaportes": nopagado})


@login_required
@user_passes_test(lambda u: u.is_staff)
def add_user(request):
    if request.method == 'POST' and 'user' in request.POST:
        if len(Usuario.objects.filter(usuario=request.POST['user'])) == 0:
            Usuario.objects.create(usuario=request.POST['user'])
            messages.add_message(request, messages.INFO,
                                 "Usuario " + request.POST['user'] + " creado satisfactoriamente")
        else:
            messages.add_message(request, messages.ERROR, "Ya existe un usuario con este nombre")
    return render(request, 'adduser.html', {'usuarios': Usuario.objects.all()})


@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_user(request, uid):
    if request.method == 'POST' and 'user' in request.POST:
        usuario = Usuario.objects.get(id=uid)

        for aporte in HistorialPagos.objects.filter(usuario=usuario.usuario):
            aporte.usuario = request.POST['user']
            aporte.save()

        usuario.usuario = request.POST['user']
        usuario.save()
        messages.add_message(request, messages.INFO,
                             "Usuario " + request.POST['user'] + " guardado satisfactoriamente")

    return render(request, 'edituser.html', {'usuario': Usuario.objects.get(id=uid)})


@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_user(request, uid):
    try:
        Usuario.objects.get(id=uid).delete()
        messages.add_message(request, messages.INFO, "Usuario eliminado satisfactoriamente")
    except:
        messages.add_message(request, messages.INFO, "Error eliminando usuario")

    return HttpResponseRedirect('/adduser')


def historial_aporte(request, year=None):
    result = []
    anhos = []
    row_total = [["Total", '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'],
                 [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-']]

    for usuario in HistorialPagos.objects.values('usuario').distinct():
        aux = [[usuario['usuario'], '-'], ['-', '-'], ['-', '-'], ['-', '-'], ['-', '-'], ['-', '-'], ['-', '-'],
               ['-', '-'], ['-', '-'], ['-', '-'], ['-', '-'], ['-', '-'], ['-', '-'], [0, '-']]
        total = 0
        if year:
            ano = year
        else:
            ano = date.today().year

        for historial in HistorialPagos.objects.filter(usuario=usuario['usuario'], ano=ano).order_by('mes'):
            aux[historial.mes] = [historial.aporte, historial.comentarios]
            total += historial.aporte
            row_total[historial.mes][0] += historial.aporte

        for i in HistorialPagos.objects.values('ano').distinct():
            if i['ano'] not in anhos:
                anhos.append(i['ano'])

        if not date.today().year in anhos:
            anhos.append(date.today().year)

        aux[13][0] = total
        row_total[13][0] += total
        result.append(aux)

    result.append(row_total)

    return render(request, "historial_aporte.html", {"aporte": result, "anhos": anhos})


@login_required
def pagar(request, uid=None):
    selected = 0
    if request.method == 'POST':
        if 'user' in request.POST and 'cantidad' in request.POST and request.POST['cantidad'] != '' \
                and 'mes' in request.POST and 'anho' in request.POST:
            if float(request.POST['cantidad']) <= 0:
                messages.add_message(request, messages.ERROR, "Ha introducido una cantidad no valida")
            else:
                aporte = Usuario.objects.get(id=int(request.POST['user']))

                if 'comentarios' in request.POST:
                    aporte.comentarios = request.POST['comentarios']
                    comentarios = request.POST['comentarios']
                else:
                    comentarios = '-'

                if len(HistorialPagos.objects.filter(mes=int(request.POST['mes']), ano=int(request.POST['anho']),
                                                     usuario=aporte.usuario)) == 0:
                    HistorialPagos(usuario=aporte.usuario, aporte=float(request.POST['cantidad']),
                                   mes=int(request.POST['mes']), ano=int(request.POST['anho']),
                                   comentarios=comentarios).save()

                    total = AporteTotal.objects.all()[0]
                    total.aporte += float(request.POST['cantidad'])

                    total.save()
                    messages.add_message(request, messages.INFO, "Aporte registrado correctamente")
                else:
                    messages.add_message(request, messages.ERROR, "Este usuario ya ha pagado este mes")
                next_id = 0
                aportes = Usuario.objects.all()
                for i in range(0, len(aportes)):
                    if aporte == aportes[i] and i != len(aportes) - 1:
                        try:
                            next_id = aportes[i + 1].id
                        finally:
                            break
                return HttpResponseRedirect('/pagar/' + str(next_id))
        else:
            messages.add_message(request, messages.ERROR, "Datos insuficientes para realizar aporte")

    usuarios = Usuario.objects.all()

    if uid is not None:
        try:
            selected = Usuario.objects.get(id=uid).usuario
        except:
            selected = None
    elif len(usuarios) > 0:
        selected = usuarios[0].usuario

    return render(request, 'pagar.html', {'selected': selected, 'usuarios': usuarios, 'mes': date.today().month,
                                          'anhos': [date.today().year - 1, date.today().year, date.today().year + 1],
                                          'currenty': date.today().year})


@login_required
@user_passes_test(lambda u: u.is_staff)
def restart(request):
    if len(HistorialPagos.objects.filter(mes=date.today().month, ano=date.today().year)) > 0:
        messages.add_message(request, messages.ERROR,
                             "Ya se ha realizado un cierre este mes. No puede realizar dos cierres el mismo mes.")
    else:
        for i in Usuario.objects.all():
            if i.comentarios:
                comentarios = i.comentarios
            else:
                comentarios = '-'
            HistorialPagos(usuario=i.usuario, aporte=i.aporte, mes=date.today().month, ano=date.today().year,
                           comentarios=comentarios).save()
            i.aporte = 0
            i.save()
        messages.add_message(request, messages.INFO, "Se ha reiniciado el mes")

    return HttpResponseRedirect('/')


def gastos(request):
    if request.method == 'POST':
        if not request.user.is_staff:
            messages.add_message(request, messages.ERROR, "Solo un administrador puede introducir gastos")
        elif 'motivo' in request.POST and 'cantidad' in request.POST and request.POST['cantidad'] != '' \
                and request.POST['motivo'] != '':
            if float(request.POST['cantidad']) <= 0:
                messages.add_message(request, messages.ERROR, "Ha introducido una cantidad no valida")
            else:
                HistorialGastos(motivo=request.POST['motivo'], cantidad=float(request.POST['cantidad'])).save()
                total = AporteTotal.objects.all()[0]
                total.aporte -= float(request.POST['cantidad'])
                total.save()
                messages.add_message(request, messages.INFO, "Gasto agregado correctamente")
        else:
            messages.add_message(request, messages.ERROR, "Datos insuficientes para introducir un gasto")

    return render(request, 'historial_gastos.html', {'gastos': HistorialGastos.objects.all()})


@login_required
@user_passes_test(lambda u: u.is_staff)
def subsanar_gasto(request, id):
    try:
        gasto = HistorialGastos.objects.get(id=id)
        total = AporteTotal.objects.all()[0]
        total.aporte += gasto.cantidad
        total.save()
        gasto.delete()
        messages.add_message(request, messages.INFO, "Se ha subsanado correctamente el gasto")
    except:
        messages.add_message(request, messages.INFO, "No se puede subsanar el gasto")

    return HttpResponseRedirect('/gastos')


@login_required
def undo(request, uid):
    try:
        aporte = HistorialPagos.objects.get(id=uid)
        total = AporteTotal.objects.all()[0]
        total.aporte -= aporte.aporte
        total.save()
        aporte.delete()
        messages.add_message(request, messages.INFO, "El aporte ha sido retirado")
    except:
        messages.add_message(request, messages.ERROR, "Error intentando deshacer este aporte")
    return HttpResponseRedirect('/')


def login_user(request):
    if request.user.is_authenticated():
        messages.add_message(request, messages.INFO, "Ya se encuentra autenticado")
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        if 'user' in request.POST and 'password' in request.POST:
            user = authenticate(username=request.POST['user'], password=request.POST['password'])

            if user is not None:
                login(request, user)
                messages.add_message(request, messages.INFO, "Bienvenido " + user.username)
                return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.ERROR, "Credenciales incorrectas")

    return render(request, 'login.html')


@login_required
def logout_user(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Ha salido correctamente")
    return HttpResponseRedirect('/')
