from utils.settings import CAFFE_PATH, DPLOY_MODEL_FILE, \
    TRAIN_MODEL_FILE, PRETRAINED, BASE_SHAPE
import sys
sys.path.append(CAFFE_PATH)

import caffe

try:
    import cv2
except ImportError as E:
    import cv as cv2

import numpy as np
import os
# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
IMAGE_FILE = 'PT0.ST0.SE1.IM9_180'

caffe.set_mode_cpu()
net = caffe.Net(DPLOY_MODEL_FILE, caffe.TEST)
                # 'model/convnet.prototxt', caffe.TEST)
                # DPLOY_MODEL_FILE, caffe.TEST)
                # '/home/lennin92/dicom/caffe/caffe_sgd_iter_24.caffemodel',
                # caffe.TEST)

# '/home/lennin92/dicom/caffe/caffe_iter_4000.caffemodel',
print "NET INFO:"
print "NET.INPUTS = ", net.inputs
print "NET.PARAMS = ", net.params
print "NET.LAYERS:"
for bl in net.blobs:
    print "    BLOB '%s' SHAPE "%(bl), [s for s in net.blobs[bl].shape]

# plt.imshow(input_image)
img = cv2.imread('prbdata/' + IMAGE_FILE + '.png', cv2.IMREAD_GRAYSCALE)
print 'img shape = ',img.shape
cv2.imwrite("prbdata/plots/input_%s.png"%(IMAGE_FILE), 255*img)
img.resize(BASE_SHAPE)
print 'img after reshape = ',img.shape
# img_blobinp = img[np.newaxis, np.newaxis, :, :]
# net.blobs['image'].reshape(*img_blobinp.shape)
net.blobs['data'].data[...] = img
cv2.imwrite("prbdata/plots/data_%s.png"%(IMAGE_FILE), 255*net.blobs['data'].data[0,0])

for bl in net.blobs:
    net.forward()
    shape = [s for s in net.blobs[bl].shape]
    for i in range(shape[1]):
        path = os.path.join('prbdata/plots/'+IMAGE_FILE, bl)
        if(not os.path.exists(path)): os.makedirs(path)
        cv2.imwrite(path+"/%d.png"%(i), 255*net.blobs[bl].data[0,i])
