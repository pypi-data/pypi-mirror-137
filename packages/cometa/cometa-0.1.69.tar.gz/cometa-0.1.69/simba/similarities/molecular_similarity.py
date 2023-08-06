from simba.similarities.abstract_similarity import Similarity,CachedSimilarity
from simba.entities.representation import RepresentationsDB
from simba.entities.molecule import sibMol
import simba.constants as CONST

# Module used by biolgoical Similarity
from tensorflow.keras.models import load_model
import pickle
import numpy as np
from scipy.sparse import csr_matrix

#Building the matrix
def build_dense_matrix_from_pair(s1,s2,ncol):
    p1_x = list(s1)
    p2_x = list(s2)
    x_idx = p1_x+[x + ncol/2 for x in p2_x]
    y_idx = ([0]*(len(p1_x)+len(p2_x)))
    X = csr_matrix((np.ones((len(x_idx),)), (y_idx,x_idx)), shape=(1,ncol))
    return X

def build_dense_matrix_from_pairs(ls1,ls2,ncol):
    x_coord = [None]*len(ls1)
    y_coord = [None]*len(ls1)
    idx = 0
    for s1,s2 in zip(ls1,ls2):
        p1_x = list(s1)
        p2_x = list(s2)
        x_idx = p1_x+[x + ncol/2 for x in p2_x]
        # x_idx_rev = p2_x+[x + ncol/2 for x in p1_x]
        # x_idx = x_idx + x_idx_rev
        y_idx = ([idx]*(len(p1_x)+len(p2_x)))
        x_coord[idx] = x_idx
        y_coord[idx] = y_idx
        idx += 1
    x_axis = np.concatenate(x_coord)
    y_axis = np.concatenate(y_coord)
    X = csr_matrix((np.ones(x_axis.shape), (y_axis,x_axis)), shape=(len(ls1), ncol))
    return X

class MolecularSimilarity(Similarity):
    def __init__(self,representation):
        self.representation=representation
        super(MolecularSimilarity,self).__init__(CONST.sim_mol_dice,sibMol)

class DiceSimilarity(MolecularSimilarity):
    def __init__(self,representation,fingerprints=None):
        if fingerprints is None:
            fingerprints=["MORGAN_ECFP","MACCS"]
        super(DiceSimilarity,self).__init__(representation)
        self.representation.reduce_structural_fingerprints(fingerprints)
        self.size = len(self.representation.representations_index["struct-fingerprints"])


    def computeSimilarity(self,o1,o2):
        s1 = self.representation[o1,"struct-fingerprints"]
        s2 = self.representation[o2,"struct-fingerprints"]
        lcommon = len(s1.keys()&s2.keys())
        return lcommon/(0.5*(len(s1)+len(s2)))

class TanimotoSimilarity(MolecularSimilarity):
    def __init__(self,representation):
        self.name = CONST.sim_mol_tanimoto
        self.representation = representation
        self.size = len(self.representation.representations_index["struct-fingerprints"])


    def computeSimilarity(self,o1,o2):
        s1 = self.representation[o1,"struct-fingerprints"]
        s2 = self.representation[o2,"struct-fingerprints"]
        lcommon = len(s1.keys()&s2.keys())
        return lcommon/(len(s1)+len(s2)-lcommon)

# At the moment the implementation is  a tensorflow model, with 2 doucle.
class BiologicalSimilarity(MolecularSimilarity):
    def __init__(self,representation,model=None):
        if model is None:
            model = CONST.path_model_biological
        self.model = load_model(model)
        super(BiologicalSimilarity,self).__init__(representation)
        self.size = len(self.representation.representations_index["struct-fingerprints"])

    def computeSimilarity(self,o1,o2):
        if isinstance(o1,list):
            s1 = [self.representation[so1,"struct-fingerprints"] for so1 in o1]
            s2 = [self.representation[so2,"struct-fingerprints"] for so2 in o2]
            X = build_dense_matrix_from_pairs(s1,s2,2*self.size)
        else:
            s1 = self.representation[o1,"struct-fingerprints"]
            s2 = self.representation[o2,"struct-fingerprints"]
            X = build_dense_matrix_from_pair(s1,s2,2*self.size)
        similarities = self.model.predict(X)
        return similarities


class CachedTanimotoSimilarity(CachedSimilarity):
    def __init__(self,representation):
        ts = TanimotoSimilarity(representation = representation)
        super().__init__(ts)
    def compute_key(self,obj):
        return obj.get_id()



if __name__=="__main__":
    PATH_STORAGE = "SimBa/data/representations"
    rdb = RepresentationsDB(PATH_STORAGE)
    rdb.reduce_structural_fingerprints(["MORGAN_ECFP3"])
    m1 = sibMol("CC(=O)C(=O)[O-]") #pyruvta
    m2 = sibMol("CC(=O)SCCNC(=O)CCNC(=O)C(C(C)(C)COP(=O)(O)OP(=O)(O)OCC1C(C(C(O1)N2C=NC3=C(N=CN=C32)N)O)OP(=O)(O)O)O") #Acetyl coa
    m3 = sibMol("C([C@@](COC(CCCCCCCCC/C=C\CCCCCC)=O)(OC(CCCCCCCCCCCCCCC)=O)[H])OC(CCCCCCC/C=C\CCCCCCCC)=O")

    s1 = rdb[m1,"struct-fingerprints"]
    s2 = rdb[m2,"struct-fingerprints"]
    s3 = rdb[m3,"struct-fingerprints"]
    ds = DiceSimilarity(rdb)
    ds[metabolites[100],metabolites[1000]]
    len(rdb.representations_index["struct-fingerprints"])

    bs = BiologicalSimilarity(rdb)
    # %timeit bs[m1,m2]
    # 0.00851*(5000*5000)
    # bs[m1,m3]
