from utils.settings import CAFFE_PATH, MODEL_FILE, PRETRAINED, SIZE
import sys
sys.path.append(CAFFE_PATH)

import caffe
import cv2
import numpy as np

# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
IMAGE_FILE = '/home/lennin92/git/peppers/prbdata/PT0.ST0.SE1.IM0_90'

caffe.set_mode_cpu()
net = caffe.Net('/home/lennin92/dicom/caffe/deploy.prototxt', caffe.TEST)

# '/home/lennin92/dicom/caffe/caffe_iter_4000.caffemodel',

print "net.inputs =", net.inputs
print "dir(net.blobs) =", dir(net.blobs)
print "dir(net.params) =", dir(net.params)
print "conv shape = ", net.blobs['conv1'].data.shape

# plt.imshow(input_image)
img = cv2.imread(IMAGE_FILE, cv2.IMREAD_COLOR)
img.resize((3, SIZE, SIZE, ))
# img_blobinp = img[np.newaxis, np.newaxis, :, :]
# net.blobs['image'].reshape(*img_blobinp.shape)
net.blobs['image'].data[...] = img

net.forward()


for i in range(63):
    cv2.imwrite('/home/lennin92/git/peppers/prbdata/plots/conv1/PT0.ST0.SE2.IM16_' + str(i) + '.jpg', 255*net.blobs['conv1'].data[0,i])

net.forward()
cv2.imwrite('/home/lennin92/git/peppers/prbdata/plots/pool1/PT0.ST0.SE2.IM16_' + str(i) + '.jpg', 255*net.blobs['pool1'].data[0,0])

net.forward()
for i in range(115):
    cv2.imwrite('/home/lennin92/git/peppers/prbdata/plots/conv2/PT0.ST0.SE2.IM16_' + str(i) + '.jpg', 255*net.blobs['conv2'].data[0,i])

net.forward()
cv2.imwrite('/home/lennin92/git/peppers/prbdata/plots/norm2/PT0.ST0.SE2.IM16_' + str(i) + '.jpg', 255*net.blobs['norm2'].data[0,0])

net.forward()
for i in range(171):
    cv2.imwrite('/home/lennin92/git/peppers/prbdata/plots/conv3/PT0.ST0.SE2.IM16_' + str(i) + '.jpg', 255*net.blobs['conv3'].data[0,i])

net.forward()
cv2.imwrite('/home/lennin92/git/peppers/prbdata/plots/pool2/PT0.ST0.SE2.IM16_' + str(i) + '.jpg', 255*net.blobs['pool2'].data[0,0])
