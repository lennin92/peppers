from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseBadRequest
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import routers

from rest.models import Clasificacion, Imagen, SugerenciaDiagnostico, CorreccionDiagnostico
from rest.serializers import ClasificacionSerializer, SugerenciaSerializer, CorreccionSerializer

import random


def analizar_estudio(id_estudio, id_serie, id_objeto=None):
    print("Analizando estudio")
    imagenes = Imagen.objects.filter(id_estudio=id_estudio, id_serie=id_serie)
    clasificaciones = Clasificacion.objects
    sugerencias = []
    for i in imagenes:
        s = SugerenciaDiagnostico()
        s.imagen = i
        s.clasificacion = clasificaciones.get(id=random.randint(0, 4))
        s.save()
        sugerencias.append(s)
    return sugerencias


class ClasificacionViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Clasificacion.objects.all()
        serializer = ClasificacionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Clasificacion.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ClasificacionSerializer(user)
        return Response(serializer.data)


class SugerenciaDiagnosticoViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        if pk is None:
            raise HttpResponseBadRequest()
        queryset = analizar_estudio(pk)
        serializer = SugerenciaSerializer(queryset, many=True)
        return Response(serializer.data)


class CorreccionDiagnosticoViewSet(viewsets.ViewSet):

    def create(self, request):
        user = request.user
        serializer = CorreccionSerializer(many=True, data=request.data)
        if serializer.is_valid():
            c = self.get_object()
            c.save()
            return Response({'status': 'correccion almacenada'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


router = routers.DefaultRouter()
router.register(r'clasificacion', ClasificacionViewSet, base_name='clasificacion')
router.register(r'sugerencia', SugerenciaDiagnosticoViewSet, base_name='sugerencia')
router.register(r'correccion', CorreccionDiagnosticoViewSet, base_name='correccion')

