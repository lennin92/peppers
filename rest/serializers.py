from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest.models import Clasificacion, CorreccionDiagnostico, SugerenciaDiagnostico, Imagen, Estudio


class ClasificacionSerializer(ModelSerializer):
    class Meta:
        model = Clasificacion
        fields = (
            'id',
            'etiqueta',
            'descripcion'
        )


class EstudioSerializer(ModelSerializer):
    class Meta:
        model = Estudio
        fields = (
            'id', 
        )


class ImagenSerializer(ModelSerializer):
    class Meta:
        model = Imagen
        fields = (
            'nombre',
            'estudio',
            'id_serie',
            'imagen_id'
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

