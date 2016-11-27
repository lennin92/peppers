from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, CharField, ListField, Serializer
from rest.models import Clasificacion, CorreccionDiagnostico, SugerenciaDiagnostico, Imagen, Estudio

class SeriesRequestSerializer(Serializer):
    seriesUID = CharField(max_length=55, allow_blank=False, trim_whitespace=True)
    objects = ListField(
            child=CharField(max_length=55, allow_blank=False, trim_whitespace=True)
        )
    

class StudyRequestSerializer(Serializer):
    studyUID = CharField(max_length=55, allow_blank=False, trim_whitespace=True)
    series = SeriesRequestSerializer(many=True)

    
class ClasificacionSerializer(ModelSerializer):
    class Meta:
        model = Clasificacion
        fields = (
            'id',
            'etiqueta',
            'descripcion'
        )

class ImagenSerializer(ModelSerializer):
    class Meta:
        model = Imagen
        fields = (
            'studyUID',
            'seriesUID',
            'objectUID',
            'nombre'
        )


class SugerenciaSerializer(ModelSerializer):
    imagen = ImagenSerializer(many=False)
    clasificacion = ClasificacionSerializer(many=False)

    class Meta:
        model = SugerenciaDiagnostico
        fields = (
            'id',
            'imagen',
            'clasificacion',
            'es_correcto'
        )


class CorreccionSerializer(ModelSerializer):
    clasificacion_correcta = ClasificacionSerializer(many=False)

    class Meta:
        model = CorreccionDiagnostico
        fields = (
            'sugerencia_id',
            'clasificacion_correcta',
            'observacion'
        )

