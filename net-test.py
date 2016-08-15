from utils.settings import CAFFE_PATH, MODEL_FILE, PRETRAINED, SIZE
import sys
sys.path.append(CAFFE_PATH)

import caffe
import cv2
import numpy as np

# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
IMAGE_FILE = 'prbdata/PT0.ST0.SE1.IM8'

caffe.set_mode_cpu()
net = caffe.Net('model/convnet.prototxt', caffe.TEST)
                # '/home/lennin92/dicom/caffe/caffe_sgd_iter_24.caffemodel',
                # caffe.TEST)

# '/home/lennin92/dicom/caffe/caffe_iter_4000.caffemodel',
print("NET INFO:")
print("NET.INPUTS = ", net.inputs)
print("NET.PARAMS = ", net.params)
print("NET.LAYERS:")
for(bl in net.blobs):
    print("\t BLOB '%s' SHAPE '%s'"%(bl, net.blobs[bl].shape))

# plt.imshow(input_image)
img = cv2.imread(IMAGE_FILE, cv2.IMREAD_COLOR)
img.resize((1, SIZE, SIZE, ))
# img_blobinp = img[np.newaxis, np.newaxis, :, :]
# net.blobs['image'].reshape(*img_blobinp.shape)
net.blobs['data'].data[...] = img

net.forward()


for i in range(63):
    cv2.imwrite('/home/lennin92/git/peppers/prbdata/plots/conv1/1PT0.ST0.SE1.IM8_' + str(i) + '.png', 255*net.blobs['conv1'].data[0,i])

net.forward()
cv2.imwrite('/home/lennin92/git/peppers/prbdata/plots/pool1/1PT0.ST0.SE1.IM8_' + str(i) + '.png', 255*net.blobs['pool1'].data[0,0])

net.forward()
for i in range(115):
    cv2.imwrite('/home/lennin92/git/peppers/prbdata/plots/conv2/1PT0.ST0.SE1.IM8_' + str(i) + '.png', 255*net.blobs['conv2'].data[0,i])

net.forward()
cv2.imwrite('/home/lennin92/git/peppers/prbdata/plots/norm2/1PT0.ST0.SE1.IM8_' + str(i) + '.png', 255*net.blobs['norm2'].data[0,0])

net.forward()
for i in range(171):
    cv2.imwrite('/home/lennin92/git/peppers/prbdata/plots/conv3/1PT0.ST0.SE1.IM8_' + str(i) + '.png', 255*net.blobs['conv3'].data[0,i])

net.forward()
cv2.imwrite('/home/lennin92/git/peppers/prbdata/plots/pool2/1PT0.ST0.SE1.IM8_' + str(i) + '.png', 255*net.blobs['pool2'].data[0,0])
