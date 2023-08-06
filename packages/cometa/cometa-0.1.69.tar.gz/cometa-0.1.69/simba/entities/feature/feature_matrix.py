from scipy.sparse import csr_matrix



class FingerprintMatrix:
    def __init__(self,nfeatures=None):
        self.nfeatures = nfeatures

    def build_matrix(self,fingerprints):
        nsamples = len(fingerprints)
        ndim = self.nfeatures

        ###Building the sprse matrix
        rows = [[idx]*len(item) for idx,item in enumerate(fingerprints)]
        rows = [item for sublist in rows for item in sublist]
        cols = [list(item.keys()) for item in fingerprints]
        cols = [item for sublist in cols for item in sublist]
        data = [list(item.values()) for item in fingerprints]
        data= [item for sublist in data for item in sublist]
        val_mat = csr_matrix((data, (rows, cols)), shape=(nsamples, ndim))
        return val_mat


