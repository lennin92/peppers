from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Clasificacion(models.Model):
    etiqueta = models.CharField(max_length=25)
    descripcion = models.TextField()


class Imagen(models.Model):
    id = models.CharField(max_length=55, primary_key=True)
    nombre = models.CharField(max_length=55)
    id_estudio = models.CharField(max_length=55)
    id_serie = models.CharField(max_length=55)


class SugerenciaDiagnostico(models.Model):
    imagen = models.ForeignKey('Imagen')
    clasificacion = models.ForeignKey('Clasificacion')
    es_correcto = models.BooleanField(default=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)


class CorreccionDiagnostico(models.Model):
    sugerencia = models.ForeignKey('SugerenciaDiagnostico')
    clasificacion_correcta = models.ForeignKey('Clasificacion')
    usuario = models.ForeignKey(User)
    observacion = models.TextField()
    fecha_hora = models.DateTimeField()





