import h5py
import numpy as np
import log

def create_h5(lines, pathH5, pathIndex, size):
    X = np.zeros((len(lines), 1, size, size), dtype='f4')
    y = np.zeros((len(lines), 1), dtype='f4')
    for i, l in enumerate(lines):
        l[2].resize((1,size,size,))
        X[i] = l[2]
        y[i] = l[1]
    with h5py.File(pathH5, 'w') as H:
        H.create_dataset('data', data=X)
        H.create_dataset('label', data=y)
    with open(pathIndex, 'a') as index:
        index.write(pathH5+"\n")
    print("GENERATED H5 %s "%(pathH5))
    log.info("GENERATED H5 %s "%(pathH5))
