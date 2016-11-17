from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseBadRequest
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import routers
from rest_framework.decorators import detail_route

from rest.models import Clasificacion, Imagen, SugerenciaDiagnostico, CorreccionDiagnostico, Estudio
from rest.serializers import ClasificacionSerializer, SugerenciaSerializer, CorreccionSerializer, EstudioSerializer

import random


def analizar_estudio(id_estudio):
    print("Analizando estudio")
    imagenes = Imagen.objects.filter(estudio__id=id_estudio)
    clasificaciones = Clasificacion.objects
    sugerencias = []
    for i in imagenes:
        s = SugerenciaDiagnostico()
        s.imagen = i
        s.clasificacion = clasificaciones.get(id=random.randint(0, 4))
        s.save()
        sugerencias.append(s)
    return sugerencias


class ClasificacionViewSet(viewsets.ModelViewSet):
    queryset = Clasificacion.objects.all()
    serializer_class = ClasificacionSerializer

    def list(self, request):
        queryset = Clasificacion.objects.all()
        serializer = ClasificacionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Clasificacion.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ClasificacionSerializer(user)
        return Response(serializer.data)


class SugerenciaDiagnosticoViewSet(viewsets.ModelViewSet):
    queryset = Estudio.objects.all()
    serializer_class = EstudioSerializer

    def sugerencia(self, request, pk=None):
        if pk is None:
            raise HttpResponseBadRequest()
        queryset = analizar_estudio(pk)
        serializer = SugerenciaSerializer(queryset, many=True)
        return Response(serializer.data)


class CorreccionDiagnosticoViewSet(viewsets.ModelViewSet):
    queryset = CorreccionDiagnostico.objects.all()
    serializer_class = CorreccionSerializer

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


clasificacion_list = ClasificacionViewSet.as_view({'get': 'list'})
clasificacion_detail = ClasificacionViewSet.as_view({'get': 'retrieve'})
sugerencia_detail = SugerenciaDiagnosticoViewSet.as_view({'get': 'sugerencia'})
correccion_create = CorreccionDiagnosticoViewSet.as_view({'post': 'create'})


