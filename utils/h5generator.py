import h5py
import caffe
import numpy as np
import csv
import cv2
import os
import random
from settings import SIZE, TMP_PNG_PATH, TRAIN_PATH,\
    TRAINLIST_PATH, TEST_PATH, TESTLIST_PATH, \
    CSV_PATH, BASE_PATH, CSV_TESTPNG_PATH, CSV_TRAINPNG_PATH, BATCH_SIZE
from dicomutils import dicom_to_png
import log

def listToCvs(l, csv_path):
    with open(csv_path, 'w') as csvf:
        csvw = csv.writer(csvf, delimiter=',')
        csvw.writerows(l)

def processPNG(lines, train_path, trainlist_path):
    new_lines = [(lines+[lines[0]])[i:i+BATCH_SIZE] for i in range(0, len(lines), BATCH_SIZE-1)]
    count = 0
    for lines2 in new_lines:
        print("PROCESSING BATCH %d"%(count))
        X = np.zeros((len(lines2), 1, SIZE, SIZE), dtype='f4')
        y = np.zeros((len(lines2), 1), dtype='f4')
        for i, l in enumerate(lines2):
            img = cv2.imread(l[0], cv2.IMREAD_COLOR)
            img.resize((3, SIZE, SIZE, ))
            # you may apply other input transformations here...
            X[i] = img
            y[i] = int(l[1])
        with h5py.File(train_path+"."+str(count), 'w') as H:
            H.create_dataset('data', data=X)  # note the name X given to the dataset!
            H.create_dataset('label', data=y)  # note the name y given to the dataset!
            count = count + 1
    with open(trainlist_path, 'w') as L:
        # list all h5 files you are going to use
        l = [train_path + "." + str(n) for n in range(len(new_lines))]
        for e in l:
            L.write(e + "\n")


def processCSV(csvpath, basepath, train_path, trainlist_path,
               test_path, testlist_path, pngtraincsv_path, pngtestcsv_path):
    pngs_train = [] # 70 % of training samples
    pngs_test  = [] # 70 % of training samples
    file_obj = open(csvpath, 'r')
    reader = csv.reader(file_obj)
    print("CONVERTING DICOM TO PNG")
    log.info("CONVERTING DICOM TO PNG")
    count = 0
    count_train = 0
    count_test = 0
    for row in reader:
        pngpath = os.path.join(TMP_PNG_PATH, row[0].replace("/",".").replace("\\","."))
        dcmpath = os.path.join(basepath, row[0])
        try:
            # print("GENERATING PNG FOR %s"%(dcmpath))
            # log.info("GENERATING PNG FOR %s"%(dcmpath))
            dicom_to_png(dcmpath, pngpath)
            if (random.uniform(0.0,1)<0.7):
                count_train = count_train +1
                pngs_train.append([pngpath, row[1]])
            else:
                count_test = count_test +1
                pngs_test.append([pngpath, row[1]])
            # print("GENERATED PNG %s"%(pngpath))
            # log.info("GENERATED PNG %s"%(pngpath))
            count = count + 1
            if count%150==0:
                print("GENERATED %d, TRAIN: %d, TEST %d"%(count, count_train, count_test))
                log.info("GENERATED %d, TRAIN: %d, TEST %d"%(count, count_train, count_test))
        except Exception, e:
            print("ERROR ON GENERATE DICOM", e)
            log.error(e)

    print("GENERATED %d samples, %d TRAINING, %d TEST"%(count, count_train, count_test))
    log.info("GENERATED %d samples, %d TRAINING, %d TEST"%(count, count_train, count_test))

    print("SAVING CSV TRAINING FILE")
    log.info("SAVING CSV TRAINING FILE")
    listToCvs(pngs_train, pngtraincsv_path)

    print("SAVING CSV TEST FILE")
    log.info("SAVING CSV TEST FILE")
    listToCvs(pngs_test, pngtestcsv_path)

    print("GENERATING H5 TRAINING FILE")
    log.info("GENERATING H5 TRAINING FILE")
    processPNG(pngs_train, train_path, trainlist_path)

    print("GENERATING H5 TEST FILE")
    log.info("GENERATING H5 TEST FILE")
    processPNG(pngs_test, test_path, testlist_path)

    print("FINISHED")
    log.info("FINISHED")


def pngCsvToH5(csvpath, h5path, h5list):
    print("BEGIN")
    log.info("BEGIN")
    file_obj = open(csvpath, 'r')
    reader = csv.reader(file_obj)
    png = []
    for row in reader:
        png.append([row[0], row[1]])
    print("GENERATING H5 FILE")
    log.info("GENERATING H5 FILE")
    processPNG(png, h5path, h5list)



if __name__=="__main__":
    processCSV(CSV_PATH, BASE_PATH, TRAIN_PATH,
        TRAINLIST_PATH, TEST_PATH, TESTLIST_PATH,
        CSV_TRAINPNG_PATH, CSV_TESTPNG_PATH)
    # print("CREATING TRAINING H5 PATH")
    # log.info("CREATING TRAINING H5 PATH")
    # pngCsvToH5(CSV_TRAINPNG_PATH, TRAIN_PATH, TRAINLIST_PATH)
    # print("CREATING TEST H5 PATH")
    # log.info("CREATING TEST H5 PATH")
    # pngCsvToH5(CSV_TESTPNG_PATH, TEST_PATH, TESTLIST_PATH)
