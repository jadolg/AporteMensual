import pinax
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from AporteDatabase.models import AporteMes, AporteTotal, HistorialGastos
from django.contrib import messages

def index(request):
    pagado = AporteMes.objects.filter(aporte__gt=0)
    total_mes = 0.0
    for i in pagado:
        total_mes += i.aporte

    return render(request,"index.html", {"total_mes":total_mes,"aportes":pagado, "noaportes":AporteMes.objects.filter(aporte=0)})


@login_required
@user_passes_test(lambda u: u.is_staff)
def add_user(request):
    if request.method == 'POST' and request.POST.has_key('user') and request.POST.has_key('rango') and request.POST.has_key('cant_usuarios') and request.POST['cant_usuarios'] != '':
        if len(AporteMes.objects.filter(usuario=request.POST['user'])) == 0:
            AporteMes(usuario=request.POST['user'], rango=request.POST['rango'],cant_usuarios=int(request.POST['cant_usuarios'])).save()
            messages.add_message(request, messages.INFO, "Usuario "+request.POST['user']+" creado satisfactoriamente")
        else:
            messages.add_message(request, messages.ERROR,"Ya existe un usuario con este nombre")
    return render(request, 'adduser.html', {'usuarios':AporteMes.objects.all()})


@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_user(request,uid):
    try:
        AporteMes.objects.get(id=uid).delete()
        messages.add_message(request, messages.INFO,"Usuario eliminado satisfactoriamente")
    except:
        messages.add_message(request, messages.INFO, "Error eliminando usuario")

    return HttpResponseRedirect('/adduser')


@login_required
def pagar(request, uid=None):
    selected = 0
    if request.method == 'POST':
        if request.POST.has_key('user') and request.POST.has_key('cantidad') and request.POST['cantidad'] != '':
            aporte = AporteMes.objects.get(id=int(request.POST['user']))
            aporte.aporte = float(request.POST['cantidad'])
            aporte.save()

            total = AporteTotal.objects.all()[0]
            total.aporte += float(request.POST['cantidad'])
            total.save()
            messages.add_message(request, messages.INFO, "Aporte registrado correctamente")
        else:
            messages.add_message(request, messages.ERROR, "Datos insuficientes para realizar aporte")

    usuarios = AporteMes.objects.filter(aporte=0)

    if uid is not None:
        selected = AporteMes.objects.get(id=uid).usuario
    elif len(usuarios) > 0:
        selected = usuarios[0].usuario

    return render(request, 'pagar.html', {'selected':selected,'usuarios':usuarios})


@login_required
@user_passes_test(lambda u: u.is_staff)
def restart(request):
    for i in AporteMes.objects.all():
        i.aporte = 0
        i.save()
    messages.add_message(request, messages.INFO, "Se ha reiniciado el mes")
    return HttpResponseRedirect('/')


def gastos(request):
    if request.method == 'POST':
        if not request.user.is_staff:
            messages.add_message(request, messages.ERROR, "Solo un administrador puede introducir gastos")
        elif request.POST.has_key('motivo') and request.POST.has_key('cantidad') and request.POST['cantidad'] != '' and request.POST['motivo'] != '':
            HistorialGastos(motivo=request.POST['motivo'], cantidad=float(request.POST['cantidad'])).save()
            total = AporteTotal.objects.all()[0]
            total.aporte -= float(request.POST['cantidad'])
            total.save()
            messages.add_message(request, messages.INFO, "Gasto agregado correctamente")
        else:
            messages.add_message(request, messages.ERROR, "Datos insuficientes para introducir un gasto")

    return render(request, 'historial_gastos.html', {'gastos': HistorialGastos.objects.all()})


@login_required
def undo(request, uid):
    try:
        aporte = AporteMes.objects.get(id=uid)
        total = AporteTotal.objects.all()[0]
        total.aporte -= aporte.aporte
        total.save()
        aporte.aporte = 0
        aporte.save()
        messages.add_message(request, messages.INFO, "El aporte ha sido retirado")
    except:
        messages.add_message(request, messages.ERROR, "Error intentando deshacer este aporte")
    return HttpResponseRedirect('/')


def login_user(request):
    if request.user.is_authenticated():
        messages.add_message(request, messages.INFO, "Ya se encuentra autenticado")
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        if request.POST.has_key('user') and request.POST.has_key('password'):
            user = authenticate(username=request.POST['user'], password=request.POST['password'])

            if user is not None:
                login(request, user)
                messages.add_message(request, messages.INFO, "Bienvenido " + user.username)
                return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.ERROR,"Credenciales incorrectas")

    return render(request,'login.html')


@login_required
def logout_user(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Ha salido correctamente")
    return HttpResponseRedirect('/')