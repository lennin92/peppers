
import csv, random, os
from utils.dcm import save_png, extract_grid
from utils.h5 import create_h5
from utils.settings import SIZE, TMP_PNG_PATH, \
    CSV_PATH, BASE_PATH, CSV_TESTPNG_PATH, CSV_TRAINPNG_PATH, BATCH_SIZE, H5_PATH
from utils import log
import traceback


def list_to_matrix(l, size):
    return [(l+[l[0]])[i:i+size] for i in range(0, len(l), size-1)]


def add_csv(csv_path, lines):
    lines = [l[0:2] for l in lines]
    with open(csv_path, 'a') as csvf:
        csvw = csv.writer(csvf, delimiter=' ')
        csvw.writerows(lines)


def process_matrix_list(matrix_list, base_path, h5_file_path, h5_index_path,
                        csv_png_path, fixed_size):
    pngs = []
    data = []
    for row in matrix_list:
        try:
            png_path = row[2] + ".png"
            matrix = extract_grid(os.path.join(base_path, row[0]))
            data.append([matrix, row[1]])
            save_png(matrix, png_path)
            pngs.append([png_path, row[1]])
        except Exception, e:
            print("ERROR " + str(row))
    # create_h5(data, h5_file_path, h5_index_path, fixed_size)
    add_csv(csv_png_path, pngs)


def process_dicom_csv(csv_path, base_path, png_base_path, batch_size, fixed_size,
                      h5_path, h5_index_path, png_train_csv_path, png_test_csv_path):
    # type: (str, str, str, int, int, str, str, str, str) -> None
    file_obj = open(csv_path, 'r')
    reader = csv.reader(file_obj)
    lista_train = []
    lista_test = []
    reader = [r for r in reader]
    random.shuffle(reader) # RANDOM ORDER OF DICOM
    for row in reader:
        png_path = os.path.join(png_base_path, row[0].replace("/", ".").replace("\\", "."))
        row.append(png_path)
        if random.uniform(0.0, 1) <= 0.7:
            lista_train.append(row)
        else:
            lista_test.append(row)

    # fix lista train to be list of list respecting batch size
    lista_train = list_to_matrix(lista_train, batch_size)
    lista_test = list_to_matrix(lista_test, batch_size)
    count_trainh5 = 0
    h5trp = h5_index_path + "/trainlist.txt"
    for lista in lista_train:
        h5p = h5_path + "/train.h5." + str(count_trainh5)
        process_matrix_list(lista, base_path, h5p, h5trp, png_train_csv_path, fixed_size)
        count_trainh5 += 1

    count_trainh5 = 0
    h5trp = h5_index_path + "/testlist.txt"
    for lista in lista_test:
        h5p = h5_path + "/test.h5." + str(count_trainh5)
        process_matrix_list(lista, base_path, h5p, h5trp, png_test_csv_path,fixed_size)
        count_trainh5 += 1



if __name__ == "__main__":
    process_dicom_csv(
        CSV_PATH, BASE_PATH, TMP_PNG_PATH, BATCH_SIZE, SIZE,
        H5_PATH, H5_PATH, CSV_TRAINPNG_PATH, CSV_TESTPNG_PATH
    )
