import h5py
import numpy as np
from collections import Counter
import glob
import pickle
import os

def make_feature_key(feat):
    return "f%i" % feat

def make_candidate_key(cand):
    return "c{:d}".format(cand)

def make_batch_key(batch):
    return "b%i" % batch

def make_clust_key(clust):
    return "c{:i}_feat".format(clust)

GROUP_NAME = "samples_probs"
SAMPLE_NAME = "samples"
CLUST_NAME = "clusters"
PRIOR_NAME = "priors"
CANDIDATES_NAME = "candidates"
INFOS_NAME = "infos"
CANDIDATES_INFOS_NAME = INFOS_NAME+"/candidates"
FEATURES_INFOS_NAME = INFOS_NAME+"/features"
FEATURES_INFOS_NAME = INFOS_NAME+"/features_candidates"
SAMPLE_KEY = SAMPLE_NAME+"/"+SAMPLE_NAME

# samp.attrs['links'] = self.links
# samp.attrs['num_batches'] = 0
# samp.attrs['num_by_batch'] = self.buffer_size
# samp.attrs['num_features'] = self.num_features
# samp.attrs['prob_unknown_prior'] = self.prob_unknown_prior
# samp.attrs['prob_unknown_link'] = self.prob_unknown_link

def load_pickle(path):
    with open(path,"rb") as f:
        return pickle.load(f)

class SamplesHandler:
    def __init__(self,path):
        self.f = h5py.File(path, "r")
        self.nbatches = self.f[GROUP_NAME].attrs["num_batches"]
        self.nfeatures = self.f[GROUP_NAME].attrs["num_features"]
        self.name_links = self.f[GROUP_NAME].attrs["links"].tolist()
        self.cache_prob = {}


    def get_probs(self,feat_id):
        """If None not candidates are found."""
        if feat_id>=self.nfeatures:
            raise ValueError("Specified feature ID, "+str(feat_id)+" is not valid.")
        kfeat = make_feature_key(feat_id)
        #Case of no value
        if len(self.f[GROUP_NAME][kfeat])==0:
            return None
        return np.concatenate([np.array(k) for k in self.f[GROUP_NAME][kfeat].values()])

    def get_samples(self,feat_id):
        return self.f[SAMPLE_KEY][feat_id,]

    def get_samples_dictionnary(self,feat_ids = None):
        if feat_ids is None:
            feat_ids = range(self.nfeatures)
        return [Counter(self.get_samples(ifeat)) for ifeat in feat_ids]
    
    def get_candidates(self,ifeat):
        vkey = make_feature_key(ifeat)
        if len(self.f[CANDIDATES_NAME][vkey])!=0:
            return self.f[CANDIDATES_NAME][vkey]
        else:
            return []

    def get_probs_mean(self,feat_ids = None):
        if feat_ids is None:
            feat_ids = range(self.nfeatures)
        if not isinstance(feat_ids,list):
            feat_ids = [feat_ids]
        return [np.mean(self.get_probs(ifeat),axis=0) for ifeat in feat_ids]

def compute_statistics(sh):
    ##We compute the number of different values by sample
    rlist = []
    for ifeat in range(sh.nfeatures):
        pfeat = sh.get_probs(ifeat)
        if pfeat is None:
            continue
        rlist.append(np.apply_along_axis(lambda x: len(np.unique(x)),arr=pfeat,axis=0))
    return np.concatenate(rlist)


def load_folder(dir_path):
    path_samples = glob.glob(dir_path+"/*.hdf5")[0]
    path_features = os.path.join(dir_path,"features.pickle")
    path_candidates = os.path.join(dir_path,"candidates.pickle")
    path_GA = os.path.join(dir_path,"GA.pickle")
    return SamplesHandler(path_samples),load_pickle(path_features),load_pickle(path_candidates),load_pickle(path_GA)

    

if __name__=="__main__":
    PDIR = "/home/dalexis/Documents/dev/SimBa/evaluations/datasets/metDNA_test/simba"
    sh,features,candidates = load_folder(PDIR)

