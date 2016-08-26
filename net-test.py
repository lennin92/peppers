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
IMAGE_FILE = 'PT0.ST0.SE2.IM30'

caffe.set_mode_cpu()
net = caffe.Net(DPLOY_MODEL_FILE, caffe.TEST)
                # 'model/convnet.prototxt', caffe.TEST)
                # DPLOY_MODEL_FILE, caffe.TEST)
                # DPLOY_MODEL_FILE, PRETRAINED,caffe.TEST)
                # caffe.TEST)

# '/home/lennin92/dicom/caffe/caffe_iter_4000.caffemodel',
print "NET INFO:"
print "NET.INPUTS = ", net.inputs
print "NET.PARAMS = ", net.params
print "NET.LAYERS:"
for bl in net.blobs:
    print "    BLOB '%s' SHAPE "%(bl), [s for s in net.blobs[bl].shape]
print "NET.TOTAL_PARAMS = ", sum([ (reduce(lambda x,y: x*y, p.data.shape)) for k in net.params for i,p in enumerate(net.params[k]) ])

# plt.imshow(input_image)
#img = cv2.imread('prbdata/' + IMAGE_FILE + '.png', cv2.IMREAD_GRAYSCALE)
img = caffe.io.load_image('prbdata/' + IMAGE_FILE + '.png', color=False)
print 'img shape = ',img.shape
cv2.imwrite("prbdata/plots/input_%s.png"%(IMAGE_FILE), 255*img)
img = img.reshape((1, 512,512))
print 'img after reshape = ',img.shape
# img_blobinp = img[np.newaxis, np.newaxis, :, :]
# net.blobs['image'].reshape(*img_blobinp.shape)
net.blobs['data'].data[...] = img
cv2.imwrite("prbdata/plots/data_%s.png"%(IMAGE_FILE), 255*net.blobs['data'].data[0,0])


for bl in net.blobs:
    net.forward()
    print "GENERATING '%s' IMAGES"%(bl)
    shape = [s for s in net.blobs[bl].shape]
    for i in range(shape[1]):
        try:
            path = os.path.join('prbdata/plots/'+IMAGE_FILE, bl)
            if(not os.path.exists(path)): os.makedirs(path)
            cv2.imwrite(path+"/%d.png"%(i), 255*net.blobs[bl].data[0,i])
        except Exception, e:
            print "error on generating '%s'"%(path+"/%d.png"%(i))
