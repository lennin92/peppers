
from rest.models import Imagen, Clasificacion, SugerenciaDiagnostico,\
    Estudio, Series
import random
import requests
import urlparse as url
import os
from django.conf import settings


def get_png(studyUID, seriesUID, objectUID):
    rel_path = settings.DICOM_PNG_URL_PATTERN%{'studyuid': studyUID,
                                              'seriesuid': seriesUID,
                                              'objectuid': objectUID }
    dcm_path = url.urljoin(settings.DCM4CHEE_HOSTDIR, rel_path)
    r = requests.get(dcm_path, stream=True)
    f_path = os.path.join(settings.DICOM_TMP_PATH, objectUID)
    if r.status_code == 200:
        with open(f_path, 'wb') as f:
            for chunk in r.iter_content(256):
                f.write(chunk)
        return f_path
    print(r.status_code)
    return None


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
        fpath = get_png(i.studyUID(),i.seriesUID(),i.objectUID)
        if fpath is not None: print("DOWNLOADED " + fpath)
        s.clasificacion = clasificaciones.get(id=random.randint(0, 4))
        s.save()
        sugerencias.append(s)
    return sugerencias


def get_study_object(studyUID):
    s,created = Estudio.objects.get_or_create(
        estudio=studyUID
    )
    # if not created: s.save()
    return s


def get_series_object(studyUID, seriesUID):
    st= get_study_object(studyUID)
    s,created = Series.objects.get_or_create(
        estudio=st,
        series=seriesUID
    )
    # if not created: s.save()
    return s


def get_image_object(studyUID, seriesUID, objectUID):
    se = get_series_object(studyUID, seriesUID)
    i,created = Imagen.objects.get_or_create(
        series=se,
        objectUID=objectUID,
        nombre=objectUID[0:9]
    )
    # if not created: i.save()
    return i