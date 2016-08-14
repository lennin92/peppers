import h5py
import numpy as np


def create_h5(lines, pathH5, pathIndex, size):
    X = np.zeros((len(lines), 3, size, size), dtype='f4')
    y = np.zeros((len(lines), 1), dtype='f4')
    for i, l in enumerate(lines):
        X[i] = l[0]
        y[i] = l[1]
    with h5py.File(pathH5, 'wb') as H:
        H.create_dataset('data', data=X)
        H.create_dataset('label', data=y)
    with open(pathIndex, 'a') as index:
        index.write(pathH5+"\n")
