import sys
import os
from utils.dicom_utils import dicom_anonimizer


def anominize_path(original, new):

    if os.path.isfile(new):
        raise Exception("New file already exists " + new)

    if os.path.isfile(original):
        dicom_anonimizer(original, new)
    else:
        for p in os.listdir(original):
            new_original = os.path.join(original,p)
            new_new = os.path.join(new,p)
            if not os.path.isfile(new_original) \
                and not os.path.exists(new_new):
                    os.makedirs(new_new)
            anominize_path(new_original, new_new)




original_path = sys.argv[1]
new_path = sys.argv[2]
anominize_path(original_path, new_path)
