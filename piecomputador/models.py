from django.db import models


class Procesador(models.Model):
    id_cpu = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    ruta_imagen = models.CharField(max_length=200, blank=True, null=True)
    enlace_pagina = models.CharField(max_length=200, blank=True, null=True)
    socket = models.CharField(max_length=20)
    velocidad_ghz = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    nucleos = models.IntegerField(null=True, blank=True)
    hilos = models.IntegerField(null=True, blank=True)
    marca = models.CharField(max_length=50)
    gama = models.CharField(max_length=20)


class TarjetaMadre(models.Model):
    id_mom = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    socket = models.CharField(max_length=50)
    tipo_memoria = models.CharField(max_length=50)
    cant_ranuras_memoria = models.IntegerField()
    max_memoria = models.IntegerField()
    formato = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    ruta_imagen = models.CharField(max_length=200, blank=True, null=True)
    gama = models.CharField(max_length=20)
    pci = models.SmallIntegerField()
    procesador_uso = models.ForeignKey(
        "Procesador", on_delete=models.SET_NULL, null=True, blank=True
    )
    ram_uso = models.ForeignKey(
        "Memoria", on_delete=models.SET_NULL, null=True, blank=True
    )
    grafica_uso = models.ForeignKey(
        "Grafica", on_delete=models.SET_NULL, null=True, blank=True
    )


class Memoria(models.Model):
    id_ram = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad_gb = models.SmallIntegerField()
    tipo_ddr = models.CharField(max_length=20)
    velocidad_mhz = models.IntegerField()
    marca = models.CharField(max_length=50)
    ruta_imagen = models.CharField(max_length=200, blank=True, null=True)
    gama = models.CharField(max_length=20)
    enlace_pagina = models.CharField(max_length=200, blank=True, null=True)


class Grafica(models.Model):
    id_gpu = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad_gb = models.SmallIntegerField()
    tipo_gddr = models.CharField(max_length=20)
    pci = models.SmallIntegerField()
    marca = models.CharField(max_length=50)
    ruta_imagen = models.CharField(max_length=200, blank=True, null=True)
    gama = models.CharField(max_length=20)
    enlace_pagina = models.CharField(max_length=200, blank=True, null=True)


class Usuarios(models.Model):
    id_usu = models.CharField(max_length=5, primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, blank=True, null=True)
    nombre_completo = models.CharField(max_length=100, blank=True, null=True)


class PC(models.Model):
    id_armado = models.CharField(max_length=5, primary_key=True)
    nombre_armado = models.CharField(max_length=100)
    id_procesador = models.ForeignKey(
        "Procesador", on_delete=models.SET_NULL, null=True, blank=True
    )
    id_tarjeta_madre = models.ForeignKey(
        "TarjetaMadre", on_delete=models.SET_NULL, null=True, blank=True
    )
    id_memoria_ram = models.ForeignKey(
        "Memoria", on_delete=models.SET_NULL, null=True, blank=True
    )
    id_tarjeta_grafica = models.ForeignKey(
        "Grafica", on_delete=models.SET_NULL, null=True, blank=True
    )


class Usuario_PC(models.Model):
    id_usu = models.ForeignKey("Usuarios", on_delete=models.CASCADE)
    id_armado = models.ForeignKey("PC", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("id_usu", "id_armado")
