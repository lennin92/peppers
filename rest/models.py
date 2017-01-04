from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Clasificacion(models.Model):
    etiqueta = models.CharField(max_length=25)
    descripcion = models.TextField()


class Estudio(models.Model):
    estudio = models.CharField(max_length=55)
    
    def studyUID(self): return self.estudio

    class __Meta__:
        unique_together = (("estudio", ),)


class Series(models.Model):
    estudio = models.ForeignKey('Estudio')
    series = models.CharField(max_length=55)
    
    def studyUID(self): return self.estudio.studyUID()
    
    def seriesUID(self): return self.series

    class __Meta__:
        unique_together = (("estudio", "series"),)

class Imagen(models.Model):
    series = models.ForeignKey('Series')
    nombre = models.CharField(max_length=10)
    objectUID = models.CharField(max_length=55)
    
    def studyUID(self): return self.series.studyUID()
    
    def seriesUID(self): return self.series.seriesUID()

    class __Meta__:
        unique_together = (("objectUID", "series"),)


class SugerenciaDiagnostico(models.Model):
    imagen = models.ForeignKey('Imagen')
    clasificacion = models.ForeignKey('Clasificacion')
    es_correcto = models.BooleanField(default=True)
    fecha_hora = models.DateTimeField(auto_now_add=True, blank=True)


class CorreccionDiagnostico(models.Model):
    imagen = models.ForeignKey('Imagen')
    clasificacion_correcta = models.ForeignKey('Clasificacion')
    usuario = models.ForeignKey(User, blank=True)
    observacion = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True, blank=True)

