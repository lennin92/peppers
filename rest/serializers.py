from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest.models import Clasificacion, CorreccionDiagnostico, SugerenciaDiagnostico, Imagen


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
            'nombre',
            'id_estudio',
            'id_serie'
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
    sugerencia = PrimaryKeyRelatedField(many=False, read_only=True)
    clasificacion_correcta = ClasificacionSerializer(many=False)

    class Meta:
        model = CorreccionDiagnostico
        fields = (
            'sugerencia',
            'clasificacion_correcta',
            'observacion'
        )
