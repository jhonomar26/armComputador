# En views.py
from django.shortcuts import render, redirect
from .models import Procesador, TarjetaMadre, Memoria, Grafica
from .forms import PrecioForm, ComponentesForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import *
from .forms import *
from rest_framework import viewsets
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic import (
    CreateView,
    DeleteView,
    UpdateView,
    ListView,
    DetailView,
)
from piecomputador.models import (
    Procesador,
    TarjetaMadre,
    Grafica,
    Memoria,
    Usuario_PC,
    PC,
    Usuarios,
)
from django.http import JsonResponse


def home(request):
    return render(request, "home.html")


# Inicializar los componenetes
class ComponentesForm(forms.Form):
    tarjeta_madre = forms.ChoiceField(choices=[], required=False)
    procesador = forms.ChoiceField(choices=[], required=False)
    memoria_ram = forms.ChoiceField(choices=[], required=False)
    tarjeta_grafica = forms.ChoiceField(choices=[], required=False)


def armar_pc(request):
    gama_value = "Baja"  # Valor inicial
    precio_value = "0,0 $"
    valor = "Valor"

    # Obtener las opciones para los componentes desde la base de datos
    tarjetas_madre_choices = [
        (tm.id_mom, f"{tm.nombre} - ${tm.precio}") for tm in TarjetaMadre.objects.all()
    ]
    procesadores_choices = [
        (proc.id_cpu, f"{proc.nombre} - ${proc.precio}")
        for proc in Procesador.objects.all()
    ]
    memorias_ram_choices = [
        (ram.id_ram, f"{ram.nombre} - ${ram.precio}") for ram in Memoria.objects.all()
    ]
    tarjetas_graficas_choices = [
        (gpu.id_gpu, f"{gpu.nombre} - ${gpu.precio}") for gpu in Grafica.objects.all()
    ]

    if request.method == "POST":
        precio_form = PrecioForm(request.POST)
        componentes_form = ComponentesForm(request.POST)

        if precio_form.is_valid():
            precio_entero = precio_form.cleaned_data["precio_form"]

            # Lógica para actualizar gama_value
            if 1 <= precio_entero <= 5:
                gama_value = "Baja"
                # Tarje
                tarjetas_madre_choices = [
                    (tm.id_mom, f"{tm.nombre} - {tm.precio}$")
                    for tm in (TarjetaMadre.objects.filter(gama="Baja"))
                ]
                componentes_form.fields[
                    "tarjeta_madre"
                ].choices = tarjetas_madre_choices

                # Filtra los procesadores de gama baja
                procesadores_gama_baja = Procesador.objects.filter(gama="Baja")
                procesadores_choices = [
                    (proc.id_cpu, f"{proc.nombre} - {proc.precio}$")
                    for proc in procesadores_gama_baja
                ]
                componentes_form.fields["procesador"].choices = procesadores_choices

                # Filtra las memorias RAM de gama baja
                memorias_ram_gama_baja = Memoria.objects.filter(gama="Baja")
                memorias_ram_choices = [
                    (ram.id_ram, f"{ram.nombre} - {ram.precio}$")
                    for ram in memorias_ram_gama_baja
                ]
                componentes_form.fields["memoria_ram"].choices = memorias_ram_choices

                # Filtra las tarjetas gráficas de gama baja
                tarjetas_graficas_gama_baja = Grafica.objects.filter(gama="Baja")
                tarjetas_graficas_choices = [
                    (gpu.id_gpu, f"{gpu.nombre} - {gpu.precio}$")
                    for gpu in tarjetas_graficas_gama_baja
                ]
                componentes_form.fields[
                    "tarjeta_grafica"
                ].choices = tarjetas_graficas_choices

            elif 6 <= precio_entero <= 10:
                gama_value = "Media"
                # Tarje
                tarjetas_madre_choices = [
                    (tm.id_mom, f"{tm.nombre} - {tm.precio}$")
                    for tm in (TarjetaMadre.objects.filter(gama="Media"))
                ]
                componentes_form.fields[
                    "tarjeta_madre"
                ].choices = tarjetas_madre_choices

                # Filtra los procesadores de gama Media
                procesadores_gama_Media = Procesador.objects.filter(gama="Media")
                procesadores_choices = [
                    (proc.id_cpu, f"{proc.nombre} - {proc.precio}$")
                    for proc in procesadores_gama_Media
                ]
                componentes_form.fields["procesador"].choices = procesadores_choices

                # Filtra las memorias RAM de gama Media
                memorias_ram_gama_Media = Memoria.objects.filter(gama="Media")
                memorias_ram_choices = [
                    (ram.id_ram, f"{ram.nombre} - {ram.precio}$")
                    for ram in memorias_ram_gama_Media
                ]
                componentes_form.fields["memoria_ram"].choices = memorias_ram_choices

                # Filtra las tarjetas gráficas de gama Media
                tarjetas_graficas_gama_Media = Grafica.objects.filter(gama="Media")
                tarjetas_graficas_choices = [
                    (gpu.id_gpu, f"{gpu.nombre} - {gpu.precio}$")
                    for gpu in tarjetas_graficas_gama_Media
                ]
                componentes_form.fields[
                    "tarjeta_grafica"
                ].choices = tarjetas_graficas_choices
            else:
                gama_value = "Alta"
                # Tarje
                tarjetas_madre_choices = [
                    (tm.id_mom, f"{tm.nombre} - {tm.precio}$")
                    for tm in (TarjetaMadre.objects.filter(gama="Alta"))
                ]
                componentes_form.fields[
                    "tarjeta_madre"
                ].choices = tarjetas_madre_choices

                # Filtra los procesadores de gama Alta
                procesadores_gama_Alta = Procesador.objects.filter(gama="Alta")
                procesadores_choices = [
                    (proc.id_cpu, f"{proc.nombre} - {proc.precio}$")
                    for proc in procesadores_gama_Alta
                ]
                componentes_form.fields["procesador"].choices = procesadores_choices

                # Filtra las memorias RAM de gama Alta
                memorias_ram_gama_Alta = Memoria.objects.filter(gama="Alta")
                memorias_ram_choices = [
                    (ram.id_ram, f"{ram.nombre} - {ram.precio}$")
                    for ram in memorias_ram_gama_Alta
                ]
                componentes_form.fields["memoria_ram"].choices = memorias_ram_choices

                # Filtra las tarjetas gráficas de gama Alta
                tarjetas_graficas_gama_Alta = Grafica.objects.filter(gama="Alta")
                tarjetas_graficas_choices = [
                    (gpu.id_gpu, f"{gpu.nombre} - {gpu.precio}$")
                    for gpu in tarjetas_graficas_gama_Alta
                ]
                componentes_form.fields[
                    "tarjeta_grafica"
                ].choices = tarjetas_graficas_choices

            # !Miro si cambio algun elemento en el formulario
            # Verificar si se ha cambiado la tarjeta madre
            field_name = request.POST.get("field_name")
            selected_value = request.POST.get("selected_value")
            if field_name == None:
                gama_value="NONE"
                
            else:
                gama_value = "Si estoy llegango solicitud pos"

        else:
            # El formulario no es válido, puedes manejarlo según tus necesidades
            precio_form = PrecioForm()  # Inicializa un nuevo formulario
    else:
        precio_form = PrecioForm()
        componentes_form = ComponentesForm()

    # Inicializamos las opciones del formulario
    componentes_form.fields["tarjeta_madre"].choices = tarjetas_madre_choices
    componentes_form.fields["procesador"].choices = procesadores_choices
    componentes_form.fields["memoria_ram"].choices = memorias_ram_choices
    componentes_form.fields["tarjeta_grafica"].choices = tarjetas_graficas_choices

    return render(
        request,
        "pc_list.html",
        {
            "gama_value": gama_value,
            "precio_value": precio_value,
            "precio_form": precio_form,
            "componentes_form": componentes_form,
        },
    )


def signup(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                if request.POST["password1"] == request.POST["password2"]:
                    # Registro en la tabla de Usuarios de Django
                    user = User.objects.create_user(
                        username=form.cleaned_data["username"],
                        password=form.cleaned_data["password1"],
                    )

                    # Registro en tu modelo Usuarios
                    usuario = Usuarios(
                        id_usu=form.cleaned_data["id_usu"],
                        username=form.cleaned_data["username"],
                        password=form.cleaned_data["password1"],
                        email=form.cleaned_data["email"],
                        nombre_completo=form.cleaned_data["nombre_completo"],
                    )
                    usuario.save()

                    # Autenticar y redirigir al usuario
                    login(request, user)
                    return redirect("home")
                else:
                    return render(
                        request,
                        "signup.html",
                        {
                            "form": form,
                            "error": "La contraseñas no coinciden",
                        },
                    )

            except IntegrityError as e:
                # Manejar la excepción de IntegrityError específica
                return render(
                    request,
                    "signup.html",
                    {"form": form, "error": "El usuario ya existe."},
                )
    else:
        form = RegistroForm()
    return render(request, "signup.html", {"form": form})


def tasks(request):
    return render(request, "task.html")


def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "POST":
        form = CustomInicioSesionForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            try:
                user = Usuarios.objects.get(username=username, password=password)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("armar_pc")
            except Usuarios.DoesNotExist:
                return render(
                    request,
                    "signin.html",
                    {
                        "form": form,
                        "error": "La contraseña o el usuario son incorrectos",
                    },
                )
    else:
        form = CustomInicioSesionForm()
    return render(request, "signin.html", {"form": form})


# vista que recibe el precio del formulario para implementar la logica del armado
