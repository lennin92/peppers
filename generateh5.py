
import csv, random, os
from utils.dcm import save_png, extract_grid
from utils.h5 import create_h5
from utils.settings import SIZE, TMP_PNG_PATH, \
    CSV_PATH, BASE_PATH, CSV_TESTPNG_PATH, CSV_TRAINPNG_PATH, BATCH_SIZE, H5_PATH
from utils import log
import traceback

def add_csv(csv_path, lines):
    lines = [l[0:2] for l in lines]
    with open(csv_path, 'a') as csvf:
        csvw = csv.writer(csvf, delimiter=',')
        csvw.writerows(lines)


def process_dicom_csv(csv_path, base_path, png_base_path, batch_size, fixed_size,
                      h5_path, h5_index_path, png_train_csv_path, png_test_csv_path):
    # type: (str, str, str, int, int, str, str, str, str) -> None
    pngs_train = []  # 70 % of training samples
    pngs_test = []  # 30 % of training samples
    file_obj = open(csv_path, 'r')
    reader = csv.reader(file_obj)
    count = 0
    count_train = 0
    count_test = 0
    count_error = 0
    count_trainh5 = 0
    count_testh5 = 0
    try:

        for row in reader:
            try:
                count += 1
                dicom_path = os.path.join(base_path, row[0])
                png_path = os.path.join(png_base_path, row[0].replace("/", ".").replace("\\", "."))
                pixel_matrix = extract_grid(dicom_path)
                save_png(pixel_matrix, png_path)

                if (random.uniform(0.0, 1) < 0.7):
                    count_train += 1
                    pngs_train.append([png_path, row[1], pixel_matrix])
                else:
                    count_test += 1
                    pngs_test.append([png_path, row[1], pixel_matrix])

                # IF LENGTH OF TRAIN IS >= BATCHSIZE, SAVE h5 AND RESTART LIST
                if len(pngs_train) >= batch_size:
                    create_h5(pngs_train, h5_path + "/train.h5." + str(count_trainh5),
                              h5_index_path + "/trainlist.txt", fixed_size)
                    add_csv(png_train_csv_path, pngs_train)
                    pngs_train = []
                    count_trainh5 += 1

                # IF LENGTH OF TEST IS >= BATCHSIZE, SAVE h5 AND RESTART LIST
                if len(pngs_test) >= batch_size:
                    create_h5(pngs_test, h5_path + "/test.h5." + str(count_testh5),
                              h5_index_path + "/testlist.txt", fixed_size)
                    add_csv(png_test_csv_path, pngs_test)
                    pngs_test = []
                    count_testh5 += 1

                if count % 200 == 0:
                    print("PROCESSED %d, TRAIN: %d, TEST: %d, ERROR: %d" % (count, count_train, count_test, count_error))
                    log.info("PROCESSED %d, TRAIN: %d, TEST: %d, ERROR: %d" % (count, count_train, count_test, count_error))
            except Exception, e:
                count_error += 1
                print("ERROR ON PROCESS DICOM '%s'" % (dicom_path,), e)
                log.error(e)
                traceback.print_exc()

        # IF LENGTH OF TRAIN IS >= BATCHSIZE, SAVE h5 AND RESTART LIST
        if len(pngs_train) >= 0:
            create_h5(pngs_train, h5_path + "/train.h5." + str(count_trainh5), h5_index_path + "/trainlist.txt", fixed_size)
            add_csv(png_train_csv_path, pngs_train)
            count_trainh5 += 1

        # IF LENGTH OF TEST IS >= BATCHSIZE, SAVE h5 AND RESTART LIST
        if len(pngs_test) >= batch_size:
            create_h5(pngs_test, h5_path + "/test.h5." + str(count_testh5), h5_index_path + "testlist.txt", fixed_size)
            add_csv(png_test_csv_path, pngs_test)
            count_testh5 += 1

        print("PROCESSED %d, TRAIN: %d, TEST: %d, ERROR: %d" % (count, count_train, count_test, count_error))
        log.info("PROCESSED %d, TRAIN: %d, TEST: %d, ERROR: %d" % (count, count_train, count_test, count_error))
    except Exception, e:
        count_error += 1
        print("ERROR ON PROCESS ", e)
        log.error(e)
        traceback.print_exc()


if __name__ == "__main__":
    process_dicom_csv(
        CSV_PATH, BASE_PATH, TMP_PNG_PATH, BATCH_SIZE, SIZE,
        H5_PATH, H5_PATH, CSV_TRAINPNG_PATH, CSV_TESTPNG_PATH
    )

