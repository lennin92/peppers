
from rest.models import Imagen, Clasificacion, SugerenciaDiagnostico,\
    Estudio, Series
import random
import requests
import urlparse as url
import os
from django.conf import settings
import logging
import time
import caffe
import numpy as np
import pandas as pd
from PIL import Image


class Classifier(object):
    net = None
    labels = []
    classifications = {}

    def get_classification(self, id):
        return self.classifications[id]

    def __init__(self):
        logging.info('Loading Network')
        if settings.CAFFE_GPU:
            caffe.set_mode_gpu()
        else:
            caffe.set_mode_cpu()
        self.net = caffe.Classifier(settings.CAFFE_MODEL, settings.CAFFE_WEIGHTS)
        self.clasificaciones = Clasificacion.objects.all()
        labels_df = pd.DataFrame([{
                'synset_id': c.id,
                'name': c.etiqueta
            } for c in self.clasificaciones
        ])
        self.classifications = {c.id:c for c in self.clasificaciones}
        self.labels = labels_df.sort_values(by='synset_id')['name'].values
        logging.info('Loaded Network')

    def forward(self):
        self.net.forward()

    def classify(self, image):
        try:
            starttime = time.time()
            scores = self.net.predict([image], oversample=True).flatten()
            endtime = time.time()

            indices = (-scores).argsort()[:3]
            predictions = self.labels[indices]

            # In addition to the prediction text, we will also produce
            # the length for the progress bar visualization.
            meta = [
                (i, p, '%.5f' % scores[i])
                for i, p in zip(indices, predictions)
            ]
            logging.info('result: %s', str(meta))

            return (True, meta, '%.3f' % (endtime - starttime))

        except Exception as err:
            logging.info('Classification error: %s', err)
            return (False, 'Something went wrong when classifying the '
                           'image. Maybe try another one?')


CLASSIFIER = Classifier()
CLASSIFIER.forward()


def open_im(im_path):
    im = Image.open(im_path)
    img = np.asarray(im).astype(np.float32) / 255.
    if img.ndim == 2:
        img = img[:, :, np.newaxis]
        img = np.tile(img, (1, 1, 3))
    elif img.shape[2] == 4:
        img = img[:, :, :3]
    return img


def get_png(studyUID, seriesUID, objectUID):
    rel_path = settings.DICOM_PNG_URL_PATTERN%{'studyuid': studyUID,
                                              'seriesuid': seriesUID,
                                              'objectuid': objectUID }
    dcm_path = url.urljoin(settings.DCM4CHEE_HOSTDIR, rel_path)
    print(dcm_path)
    r = requests.get(dcm_path, stream=True)
    f_path = os.path.join(settings.DICOM_TMP_PATH, objectUID+ '.png')
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
    sugerencias = []
    for i in imagenes:
        s = SugerenciaDiagnostico()
        s.imagen = i
        fpath = get_png(i.studyUID(),i.seriesUID(),i.objectUID)
        if fpath is not None:
            print("DOWNLOADED " + fpath)
            image = open_im(fpath)
            clasif_result = CLASSIFIER.classify(image)
            if clasif_result[0]:
                pred = clasif_result[1][1][0]
            else:
                logging.error("ERROR ON CLASIFING IMAGE AT " +fpath)
                pred = random.randint(0, 4)
        else:
            logging.error("ERROR GETTING IMAGE for " + i.objectUID)
            pred = random.randint(0, 4)
        s.clasificacion = CLASSIFIER.get_classification(pred)
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