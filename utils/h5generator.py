import h5py
import caffe
import numpy as np
import csv
import os

from settings import SIZE, TMP_PNG_PATH, TRAIN_PATH, TRAINLIST_PATH, CSV_PATH, BASE_PATH
from dicomutils import dicom_to_png
import traceback



def processPNG(lines, train_path, trainlist_path):
    X = np.zeros((len(lines), 3, SIZE, SIZE), dtype='f4')
    y = np.zeros((1, len(lines)), dtype='f4')
    for i, l in enumerate(lines):
        img = caffe.io.load_image(l[0])
        img = caffe.io.resize(img, (SIZE, SIZE, 3))  # resize to fixed size
        # you may apply other input transformations here...
        X[i] = img
        y[i] = int(l[1])
    with h5py.File(train_path, 'w') as H:
        H.create_dataset('X', data=X)  # note the name X given to the dataset!
        H.create_dataset('y', data=y)  # note the name y given to the dataset!
    with open(trainlist_path, 'w') as L:
        L.write(train_path)  # list all h5 files you are going to use


def processCSV(csvpath, basepath, train_path, trainlist_path):
    pngs = []
    file_obj = open(csvpath, 'r')
    reader = csv.reader(file_obj)
    for row in reader:
        pngpath = os.path.join(TMP_PNG_PATH, row[0])
        dcmpath = os.path.join(basepath, row[0])
        if not os.path.exists(pngpath):
            os.remove(pngpath)
        print("Storing %s on %s"%(dcmpath, pngpath))
        try:
            dicom_to_png(dcmpath, pngpath)
            pngs.push([pngpath, row[1]])
        except Exception, e:
            print("ERROR ON GENERATE DICOM")
            print(traceback.format_exc())
    processPNG(pngs, train_path, trainlist_path)


if __name__=="__main__":
    processCSV(CSV_PATH, BASE_PATH, TRAIN_PATH, TRAINLIST_PATH)