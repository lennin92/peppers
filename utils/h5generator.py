import h5py
import caffe
import numpy as np
import csv
import os

from settings import SIZE, TMP_PNG_PATH, TRAIN_PATH, TRAINLIST_PATH, CSV_PATH, BASE_PATH
from dicomutils import dicom_to_png
import log

def processPNG(lines, train_path, trainlist_path):
    X = np.zeros((len(lines),  3, SIZE, SIZE), dtype='f4')
    y = np.zeros((len(lines), 1), dtype='f4')
    for i, l in enumerate(lines):
        print(l)
        img = caffe.io.load_image(l[0])
        img = caffe.io.resize(img, (3, SIZE, SIZE))  # resize to fixed size
        # you may apply other input transformations here...
        X[i] = img
        y[i] = int(l[1])
    with h5py.File(train_path, 'w') as H:
        H.create_dataset('image', data=X)  # note the name X given to the dataset!
        H.create_dataset('label', data=y)  # note the name y given to the dataset!
    with open(trainlist_path, 'w') as L:
        L.write(train_path)  # list all h5 files you are going to use


def processCSV(csvpath, basepath, train_path, trainlist_path):
    pngs = []
    file_obj = open(csvpath, 'r')
    reader = csv.reader(file_obj)
    print("CONVERTING DICOM TO PNG")
    log.info("CONVERTING DICOM TO PNG")
    for row in reader:
        pngpath = os.path.join(TMP_PNG_PATH, row[0].replace("/",".").replace("\\","."))
        dcmpath = os.path.join(basepath, row[0])
        try:
            print("GENERATING PNG FOR %s"%(dcmpath))
            log.info("GENERATING PNG FOR %s"%(dcmpath))
            dicom_to_png(dcmpath, pngpath)
            pngs.append([pngpath, row[1]])
            pngs.append([pngpath, row[1]])
            print("GENERATED PNG %s"%(pngpath))
            log.info("GENERATED PNG %s"%(pngpath))
        except Exception, e:
            print("ERROR ON GENERATE DICOM", e)
            log.error(e)
    print("GENERATING H5 DATABASE FILE")
    log.info("GENERATING H5 DATABASE FILE")
    processPNG(pngs, train_path, trainlist_path)
    print("FINISHED")
    log.info("FINISHED")


if __name__=="__main__":
    processCSV(CSV_PATH, BASE_PATH, TRAIN_PATH, TRAINLIST_PATH)