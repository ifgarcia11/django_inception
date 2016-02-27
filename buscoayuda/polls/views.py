# coding=utf-8
import datetime

import boto
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import Trabajador, TrabajadorForm, UserForm
from .models import TiposDeServicio
from django.shortcuts import render
from django.contrib import messages
from django.contrib import auth


def index(request):
    trabajadores = Trabajador.objects.all()
    tipos_de_servicios = TiposDeServicio.objects.all()
    form_trabajador = TrabajadorForm(request.POST)
    form_usuario = UserForm(request.POST)
    context = {'trabajadores': trabajadores, 'tipos_de_servicios': tipos_de_servicios,
               'form_trabajador': form_trabajador, 'form_usuario': form_usuario}
    return render(request, 'polls/index.html', context)


def login(request):
    username = request.POST.get('usrname', '')
    password = request.POST.get('psw', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        messages.success(request, "Bienvenido al sistema {}".format(username), extra_tags="alert-success")
        return HttpResponseRedirect('/')
    else:
        messages.error(request, "¡El usuario o la contraseña son incorrectos!", extra_tags="alert-danger")
        return HttpResponseRedirect('/')


def logout(request):
    auth.logout(request)
    messages.info(request, "Cerraste sesión exitosamente", extra_tags="alert-info")
    return HttpResponseRedirect('/')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password=request.POST.get('password')

        user = User.objects.create_user(username=username, password=password)
        user.first_name = request.POST.get('nombre')
        user.last_name = request.POST.get('apellidos')
        user.email = request.POST.get('correo')
        user.save()

        nuevo_trabajador=Trabajador(nombre=request.POST['nombre'],
                                      apellidos=request.POST['apellidos'],
                                      aniosExperiencia=request.POST.get('aniosExperiencia'),
                                      tiposDeServicio=TiposDeServicio.objects.get(pk=request.POST.get('tiposDeServicio')),
                                      telefono=request.POST.get('telefono'),
                                      correo=request.POST.get('correo'),
                                      imagen=request.POST.get('imagen'),
                                      usuarioId=user);
        nuevo_trabajador.save()

    return HttpResponseRedirect('/')
