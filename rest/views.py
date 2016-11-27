from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from rest.models import Clasificacion, CorreccionDiagnostico, Estudio
from rest.serializers import ClasificacionSerializer, SugerenciaSerializer, CorreccionSerializer, StudyRequestSerializer
from rest import utils
from rest_framework import permissions


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
            queryset = utils.analizar_estudio(request_serializer.data)
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
            c.imagen = utils.get_image_object(i['studyUID'], i['seriesUID'], i['objectUID'])
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


