# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuarios
from django.contrib.auth.forms import AuthenticationForm


class RegistroForm(forms.Form):
    # Campos para el modelo de Usuarios de Django
    username = forms.CharField(max_length=50, label="Nombre de usuario")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="Confirmar contraseña"
    )
    
    # Campos para el modelo Usuarios
    id_usu = forms.CharField(max_length=5, label="ID de usuario")
    email = forms.EmailField(max_length=100, required=False, label="Correo electrónico")
    nombre_completo = forms.CharField(
        max_length=100, required=False, label="Nombre completo"
    )


class CustomInicioSesionForm(AuthenticationForm):
    class Meta:
        model = Usuarios
        fields = ["username", "password"]
