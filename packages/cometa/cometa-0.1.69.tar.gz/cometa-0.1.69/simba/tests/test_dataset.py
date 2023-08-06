import pandas as pd
import numpy as np
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


PATH_FEATURES =  "/home/dalexis/Documents/dev/SimBa/simba/tests/ecoli_lcms.csv"
PATH_CANDIDATES = "/home/dalexis/Documents/dev/SimBa/simba/tests/kegg_candidates.csv"

def generate_dataset(num_features=None,num_candidates=None,num_sample = 5):
    features = pd.read_csv(PATH_FEATURES)
    candidates = pd.read_csv(PATH_CANDIDATES)
    fcands = set(candidates['kegg.compound.id']).intersection(set(features['kegg.compound.id']))
    candidates = candidates[candidates['kegg.compound.id'].isin(fcands)]
    features = features[features['kegg.compound.id'].isin(fcands)]

    ##We add the fake intensity
    num_features = features.shape[0]
    log_int = np.random.beta(a=1.5,b=2,size=num_features*num_sample)*4+1
    int = 10**log_int.reshape(num_features,num_sample)

    cnames = features.columns
    int_names = ["intensity_sample"+str(i) for i in range(num_sample)]
    ifeatures = pd.concat([features,pd.DataFrame(int,columns=int_names)],axis=1)
    return ifeatures,candidates

if __name__=="__main__":
    feats,cands = generate_dataset()
    feats.shape
    cands.shape
    feats
