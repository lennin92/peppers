
import dicom, os

try:
    import cv2
except ImportError as E:
    import cv as cv2

import numpy as np


def save_png(grid, path):
    cv2.imwrite(path+".png", grid)


def extract_grid(dicom_path, normalize=True, maxval=255.0):
    with open(dicom_path,'rb') as f:
        dcm = dicom.read_file(f)
        grid = dcm.pixel_array
        if normalize:
            mx = np.max(grid)
            if mx<0:
                grid = np.zeros(grid.shape)
            else:
                grid = (grid*maxval)/mx
        return grid


def dicom_to_png(dicom_path, png_path):
    if not os.path.exists(dicom_path):
        raise Exception("Dicom Path does not exists %s" % (dicom_path))

    if os.path.exists(png_path):
        raise Exception("PNG Path already exists %s" % (png_path))

    pixel_matrix = extract_grid(dicom_path)

    save_png(pixel_matrix, png_path)