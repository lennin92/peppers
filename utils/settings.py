SIZE = 512
BASE_SHAPE = (1, SIZE, SIZE)
"""
    ENVIROMENTS = [
        (1, 'LENNIN-TOSHIBAPC'),
        (2, 'LENNIN-WORKPC'),
        (3, 'COLATO-CASA'),

    ]

"""
ENVIROMENT = 2 # 'LENNIN-TOSHIBAPC'
BATCH_SIZE = 350

if ENVIROMENT == 1: #'LENNIN-TOSHIBAPC':
    BASE_PATH = 'E:/TESIS/dicom/'
    TMP_PNG_PATH = 'E:/TESIS/png/'

    CSV_PATH = 'E:/TESIS/csv/global_prb.csv'
    CSV_TRAINPNG_PATH = 'E:/TESIS/csv/pngtrain_prb.csv'
    CSV_TESTPNG_PATH = 'E:/TESIS/csv/pngtest_prb.csv'

    H5_PATH = 'E:/TESIS/h5'

    LOG_FILE_PATH = 'E:/TESIS/log.txt'

    CAFFE_PATH = 'C:/Anaconda2/envs/peppers/Lib/site-packages/caffe'

    DPLOY_MODEL_FILE = 'model/deploy.prototxt'
    TRAIN_MODEL_FILE = 'model/train.prototxt'
    PRETRAINED = None

elif ENVIROMENT == 2: #'LENNIN-WORKPC':
    BASE_PATH = '/home/lennin92/TESIS/dicom/'
    TMP_PNG_PATH = '/home/lennin92/TESIS/png/'

    CSV_PATH = '/home/lennin92/TESIS/csv/globaltest.csv'
    CSV_TRAINPNG_PATH = '/home/lennin92/TESIS/csv/pngtrain.csv'
    CSV_TESTPNG_PATH = '/home/lennin92/TESIS/csv/pngtest.csv'

    H5_PATH = '/home/lennin92/TESIS/h5/'

    LOG_FILE_PATH = '/home/lennin92/TESIS/h5/log.txt'

    CAFFE_PATH = '~/caffe/python'

    DPLOY_MODEL_FILE = 'model/deploy.prototxt'
    TRAIN_MODEL_FILE = 'model/train.prototxt'
    PRETRAINED = '/home/lennin92/TESIS/caffe/caffe_iter_1657.caffemodel'

elif ENVIROMENT == 3: #'COLATO-CASA':
    BASE_PATH = '/home/jaco/TESIS/dicom/'
    TMP_PNG_PATH = '/home/jaco/TESIS/png/'

    CSV_PATH = '/home/jaco/TESIS/csv/globaltest.csv'
    CSV_TRAINPNG_PATH = '/home/jaco/TESIS/csv/pngtrain.csv'
    CSV_TESTPNG_PATH = '/home/jaco/TESIS/csv/pngtest.csv'

    H5_PATH = '/home/jaco/h5/'

    LOG_FILE_PATH = '/home/jaco/TESIS/h5/log.txt'

    CAFFE_PATH = '~/caffe/python'

    DPLOY_MODEL_FILE = 'model/deploy.prototxt'
    TRAIN_MODEL_FILE = 'model/train.prototxt'
    PRETRAINED = None
else:
    TMP_PNG_PATH = '/run/media/lennin92/SAMSUNG/DICOM/png/'
    H5_PATH = ''

    CSV_PATH = '/run/media/lennin92/SAMSUNG/DICOM/csv/global.csv'
    CSV_TRAINPNG_PATH = '/run/media/lennin92/SAMSUNG/DICOM/csv/pngtrain.csv'
    CSV_TESTPNG_PATH = '/run/media/lennin92/SAMSUNG/DICOM/csv/pngtest.csv'

    TRAIN_PATH = '/run/media/lennin92/SAMSUNG/DICOM/h5/train.h5'
    TRAINLIST_PATH = '/run/media/lennin92/SAMSUNG/DICOM/h5/trainlist.h5.txt'
    TEST_PATH = '/run/media/lennin92/SAMSUNG/DICOM/h5/test.h5'
    TESTLIST_PATH = '/run/media/lennin92/SAMSUNG/DICOM/h5/testlist.h5.txt'

    BASE_PATH = '/run/media/lennin92/SAMSUNG/DICOM/'

    LOG_FILE_PATH = '/run/media/lennin92/SAMSUNG/DICOM/log.txt'

    CAFFE_PATH = '~/caffe/python'

    DPLOY_MODEL_FILE = 'model/deploy.prototxt'
    TRAIN_MODEL_FILE = 'model/train.prototxt'
    PRETRAINED = '/home/lennin92/TESIS/caffe/caffe_iter_40000.caffemodel'
