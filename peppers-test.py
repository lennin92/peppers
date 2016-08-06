from utils.settings import CAFFE_PATH, MODEL_FILE, PRETRAINED
import sys
sys.path.append(CAFFE_PATH)

import numpy as np

import caffe

# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
IMAGE_FILE = '/home/lennin/peppers/prbdata/PT0.ST0.SE1.IM16'

caffe.set_mode_cpu()
net = caffe.Classifier(MODEL_FILE, PRETRAINED,
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))
input_image = caffe.io.load_image(IMAGE_FILE)
# plt.imshow(input_image)

prediction = net.predict([input_image])  # predict takes any number of images, and formats them for the Caffe net automatically
print 'prediction shape:', prediction[0].shape
# plt.plot(prediction[0])
print 'predicted class:', prediction[0].argmax()
# plt.show()