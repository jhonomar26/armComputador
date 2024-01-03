# En views.py
from django.shortcuts import render, redirect
from .models import Procesador, TarjetaMadre, Memoria, Grafica
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import *
from .forms import *


def home(request):
    return render(request, "home.html")


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
                    return redirect("tasks")
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
