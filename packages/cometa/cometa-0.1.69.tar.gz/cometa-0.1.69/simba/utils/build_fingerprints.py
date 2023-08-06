import numpy as np
from scipy.sparse import csr_matrix


def build_dense_matrix_from_fingerprints(fingerprints,ncol):
    x_coord = [None]*len(fingerprints)
    y_coord = [None]*len(fingerprints)
    idx = 0
    for ff in fingerprints:
        x_idx = list(ff)
        y_idx = ([idx]*len(x_idx))
        x_coord[idx] = x_idx
        y_coord[idx] = y_idx
        idx += 1
    x_axis = np.concatenate(x_coord)
    y_axis = np.concatenate(y_coord)
    X = csr_matrix((np.ones(x_axis.shape), (y_axis,x_axis)), shape=(len(fingerprints), ncol))
    return X
