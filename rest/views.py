from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseBadRequest
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from rest.models import Clasificacion, Imagen, SugerenciaDiagnostico, CorreccionDiagnostico, Estudio, Series
from rest.serializers import ClasificacionSerializer, SugerenciaSerializer, CorreccionSerializer, StudyRequestSerializer

import random
from rest_framework import permissions


def analizar_estudio(estudio):
    """
    Funcion que ejecuta el proceso de analisis sobre todo un estudio
    el parametro estudio es un diccionario con el siguiente esquema:

    """
    print("Analizando estudio")
    imagenes = Imagen.objects.filter(series__estudio__estudio=estudio['studyUID'])
    clasificaciones = Clasificacion.objects
    sugerencias = []
    for i in imagenes:
        s = SugerenciaDiagnostico()
        s.imagen = i
        s.clasificacion = clasificaciones.get(id=random.randint(0, 4))
        s.save()
        sugerencias.append(s)
    return sugerencias


def get_study_object(studyUID):
    s,created = Estudio.objects.get_or_create(
        estudio=studyUID
    )
    if not created: s.save()
    return s


def get_series_object(studyUID, seriesUID):
    st= get_study_object(studyUID)
    s,created = Series.objects.get_or_create(
        estudio=st,
        series=seriesUID
    )
    if not created: s.save()
    return s


def get_image_object(studyUID, seriesUID, objectUID):
    se = get_series_object(studyUID, seriesUID)
    i,created = Imagen.objects.get_or_create(
        series=se,
        objectUID=objectUID,
        nombre=objectUID[0:9]
    )
    if not created: i.save()
    return i


class ClasificacionViewSet(viewsets.ModelViewSet):
    queryset = Clasificacion.objects.all()
    serializer_class = ClasificacionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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
    serializer_class = StudyRequestSerializer
    permission_classes = (permissions.AllowAny,)

    def sugerencia(self, request):
        request_serializer = StudyRequestSerializer(many=False, data=request.data)
        if request_serializer.is_valid():
            queryset = analizar_estudio(request_serializer.data)
            serializer = SugerenciaSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid request body'},
                            status=status.HTTP_400_BAD_REQUEST)


class CorreccionDiagnosticoViewSet(viewsets.ModelViewSet):
    queryset = CorreccionDiagnostico.objects.all()
    serializer_class = CorreccionSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        user = request.user
        serializer = CorreccionSerializer(many=False, data=request.data)
        if serializer.is_valid():
            d = request.data
            i = d['imagen']
            cl = d['clasificacion_correcta']
            c = CorreccionDiagnostico()
            c.imagen = get_image_object(i['studyUID'], i['seriesUID'], i['objectUID'])
            # c.usuario = user
            c.observacion = d['observacion']
            c.clasificacion_correcta = Clasificacion.objects.get(id=cl['id'])
            c.save()
            return Response({'status': 'correccion almacenada'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


clasificacion_list = ClasificacionViewSet.as_view({'get': 'list'})
clasificacion_detail = ClasificacionViewSet.as_view({'get': 'retrieve'})
sugerencia_detail = SugerenciaDiagnosticoViewSet.as_view({'post': 'sugerencia'})
correccion_create = CorreccionDiagnosticoViewSet.as_view({'post': 'create'})


