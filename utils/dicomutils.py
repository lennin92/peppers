import os
import png
import dicom
import log

def extract_png(dicom_path):
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
    max_val = 0
    for row in __dicom__ .pixel_array:
        pixels = []
        for col in row:
            pixels.append(col)
            if col > max_val: max_val = col
        image_2d.append(pixels)
    # Rescaling grey scale between 0-255
    if max_val>0:
        image_2d_scaled = []
        for row in image_2d:
            row_scaled = []
            for col in row:
                col_scaled = int((float(col) * 255.0/ float(max_val)) )
                row_scaled.append(col_scaled) # red
                row_scaled.append(col_scaled) # green
                row_scaled.append(col_scaled) # blue
            image_2d_scaled.append(row_scaled)
        return (shape[0], shape[1], image_2d_scaled, )
    raise Exception("MAX VAL = 0")

def save_png(pixel_matix, height, width, path):
    log.info("SAVING PNG " + path)
    png_file = open(path, 'wb')
    w = png.Writer(height, width, greyscale=False)
    w.write(png_file, pixel_matix)


def dicom_to_png(dicom_path, png_path):

    if not os.path.exists(dicom_path):
        raise Exception("Dicom Path does not exists %s"%(dicom_path))

    if os.path.exists(png_path):
        raise Exception("PNG Path already exists %s"%(png_path))

    height, width, pixel_matrix = extract_png(dicom_path)

    save_png(pixel_matrix, height, width, png_path)
