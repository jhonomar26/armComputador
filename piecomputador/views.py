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
from rest_framework import viewsets


def home(request):
    return render(request, "home.html")


# componentes
class ComponentsListView(ListView):
    model = PC
    template_name = "pc_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["procesadores"] = Procesador.objects.all()
        context["tarjetas_madre"] = TarjetaMadre.objects.all()
        context["memorias_ram"] = Memoria.objects.all()
        context["tarjetas_graficas"] = Grafica.objects.all()
        return context


# # Armar pc
# class ArmarPCView(View):
#     template_name = "armar_pc.html"  # Crea un nuevo template si es necesario

#     def get(self, request, *args, **kwargs):
#         # Lógica para manejar la solicitud GET (si es necesario)
#         return render(request, self.template_name)

#     def post(self, request, *args, **kwargs):
#         # Lógica para manejar la solicitud POST y armar el PC con los componentes seleccionados
#         procesador_id = request.POST.get("procesador")
#         tarjeta_madre_id = request.POST.get("tarjeta_madre")
#         memoria_ram_id = request.POST.get("memoria_ram")

#         # Realiza la lógica para armar el PC utilizando los IDs de los componentes
#         # ...

#         pc_nuevo = PC.objects.create(
#             id_armado=100,  # Cambiar por la lógica adecuada
#             nombre_armado="armado1",  # Cambiar por la lógica adecuada
#             id_procesador_id=procesador_id,
#             id_tarjeta_madre_id=tarjeta_madre_id,
#             id_memoria_ram_id=memoria_ram_id,
#             # id_tarjeta_grafica_id=122,  # Cambiar por la lógica adecuada
#             # Completa con otros campos y valores necesarios
#         )

#         # Redirige a la página de detalles del PC recién armado o a donde desees
#         return redirect(
#             "detalle-pc", pk=pc_nuevo.id_armado
#         )  # Asegúrate de tener una URL y vista para ver los detalles de un PC

#         # Redirige a la página de detalles del PC recién armado o a donde desees


# class PCDetailView(DetailView):
#     model = PC
#     template_name = "pc_detail.html"


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
def armar_pc(request):
    precio_guardado = None

    try:
        if request.method == "POST":
            precio = request.POST.get("precio")
            # Lógica adicional y procesamiento aquí

            # Ejemplo: Simular un error
            # raise ValueError("¡Este es un error de ejemplo!")

            precio_guardado = precio

    except Exception as e:
        print(f"Error en la vista armar_pc: {e}")

    return render(request, "pc_list.html", {"precio_guardado": precio_guardado})
