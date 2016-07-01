
# MODEL DEFINITION PATHS
# MODIFY
# MUST CONTAIN PATHS TO VALID FILES

import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

MODEL_DEF_FILE = ''

PRETRAINED_MODEL_FILE = ''

MEAN_FILE = ''

CLASS_LABELS_FILE = ''

BET_FILE = ''

IMAGE_DIM = 256

RAW_SCALE = 255

GPU = False

CLASIFIER_VALUES = {
    'model_def_file' : MODEL_DEF_FILE,
    'pretrained_model_file' : PRETRAINED_MODEL_FILE,
    'mean_file' : MEAN_FILE,
    'class_labels_file' : CLASS_LABELS_FILE,
    'bet_file' : BET_FILE,
}


for k,v in CLASIFIER_VALUES:
    if os.path.exists(v):
        raise Exception("File for %s is missing. Should be at %s."%(k,v))


CLASIFIER_VALUES['image_dim'] = IMAGE_DIM
CLASIFIER_VALUES['raw_scale'] = RAW_SCALE
CLASIFIER_VALUES['gpu'] = GPU
