from django.contrib import admin
from .models import Procesador, TarjetaMadre, Memoria, Grafica, Usuarios, PC, Usuario_PC

admin.site.register(Procesador)
admin.site.register(TarjetaMadre)
admin.site.register(Memoria)
admin.site.register(Grafica)
admin.site.register(Usuarios)
admin.site.register(PC)
admin.site.register(Usuario_PC)
