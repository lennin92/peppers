from utils.settings import CAFFE_PATH, MODEL_FILE, PRETRAINED, SIZE
import sys
sys.path.append(CAFFE_PATH)

import caffe
import cv2
import numpy as np

# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
IMAGE_FILE = '/home/lennin92/git/peppers/prbdata/PT0.ST0.SE2.IM16'

caffe.set_mode_cpu()
net = caffe.Net('/home/lennin92/git/peppers/model/convnet.prototxt',caffe.TEST)

print "net.inputs =", net.inputs
print "dir(net.blobs) =", dir(net.blobs)
print "dir(net.params) =", dir(net.params)
print "conv shape = ", net.blobs['conv1'].data.shape

# plt.imshow(input_image)
img = cv2.imread(IMAGE_FILE, 0)
img_blobinp = img[np.newaxis, np.newaxis, :, :]
net.blobs['image'].reshape(*img_blobinp.shape)
net.blobs['image'].data[...] = img_blobinp

net.forward()


for i in range(96):
    cv2.imwrite('/home/lennin92/git/peppers/prbdata/plots/PT0.ST0.SE2.IM16_output_image_' + str(i) + '.jpg', 255*net.blobs['conv1'].data[0,i])
