import os
import png
import dicom
import json


DEFAULT_DATA_TO_GET = [
    'PatientSex',
    'WindowCenter',
    'SamplesPerPixel',
    'PatientBirthDate',
    'GantryDetectorTilt',
    'StudyDate',
    'PatientAge',
    'ImageType',
    'PatientPosition'
]

"""
    Format of the entry (A, B)
    where:
        - A : Tag of the data entry in the dicom file
        - B : Type of data must be a value in
            * 'STR' for string values
            * 'INT' for integer values
            * '+INT' for positive integer values
            * '-INT' for negative integer values
"""
DEFAULT_DATA_TO_ANONIMIZE = [
    ('PatientID', 'STR'),
    ('PatientName', 'STR')
]

def genRamdomData(type):
    if type=='STR':
        return 'ASDASDAS ASDASDASD'
    if type=='INT':
        return 11220
    if type=='FLOAT':
        return 22.21
    return ''

def save_png(pixel_matix, height, width, path):
    png_file = open(path, 'wb')
    w = png.Writer(height, width, greyscale=True)
    w.write(png_file, pixel_matix)


def save_data(dict, path):
    with open(path, 'w') as fp:
        json.dump(dict, fp)


def extract_dicom_data(dicom_path, data_to_get):
    """
        Function that extracts the dicom data in a tuple in format (A,B,C)
        where:
            A : height of the dicom image
            B : width of the dicom image
            C : dicom image in matrix format
    """
    # Extracting data from the mri file
    dicom_file = open(dicom_path, 'rb')
    __dicom__ = dicom.read_file(dicom_file)
    shape = __dicom__.pixel_array.shape

    image_2d = []
    for row in __dicom__.pixel_array:
        pixels = []
        for col in row:
            pixels.append(col)
        image_2d.append(pixels)
    return (shape[0], shape[1], image_2d, extract_data(dicom_file, data_to_get))


def extract_data(dicom_file, data_to_get):
    """
        Function returns a dict with the values
        of the dicom data in dicom_file that
        corresponds to the list data_to_get.
    """
    dicom = dicom_file
    return {
        key: dicom.data_element(key).tag for key in data_to_get if key in dicom
    }


def dicom_to_png(dicom_path, png_path, data_path=None, data_to_get=DEFAULT_DATA_TO_GET):

    if data_path is not None and data_to_get is None:
        raise Exception("If data_path is defined, data_to_get must be defined too")

    if not os.path.exists(dicom_path):
        raise Exception("Dicom Path does not exists")

    if os.path.exists(png_path):
        raise Exception("PNG Path already exists")

    if data_path is not None and os.path.exists(data_path):
        raise Exception("Data Path already exists")

    height, width, pixel_matrix, dicom_data = extract_dicom_data(dicom_path)

    save_png(pixel_matrix, height, width, png_path)

    if data_path is not None:
        save_data(dicom_data, data_path)


def dicom_anonimizer(original_dicom_path, new_dicom_path, data_to_anonimize=DEFAULT_DATA_TO_ANONIMIZE):
    dicom_file = open(original_dicom_path, 'rb')
    __dicom__ = dicom.read_file(dicom_file)

    for e in data_to_anonimize:
        __dicom__.data_element(e[0]).value = genRamdomData(e[1])
    new_dicom = open(new_dicom_path, 'wb')
    __dicom__.save_as(new_dicom)


def get_dicom_array(dicom_path):
    dicom_data = extract_dicom_data(dicom_path)
    return dicom_data[2]
