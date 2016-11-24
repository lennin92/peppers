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
    clasificacion_correcta = ClasificacionSerializer(many=False)

    class Meta:
        model = CorreccionDiagnostico
        fields = (
            'sugerencia_id',
            'clasificacion_correcta',
            'observacion'
        )

