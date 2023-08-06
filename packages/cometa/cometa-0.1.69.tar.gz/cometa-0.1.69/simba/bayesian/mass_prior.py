from evaluations.src.simba_annot import PRIOR_NAME
import numpy as np
from simba.bayesian.mixture_similarity import get_estimators

def get_mass_diff(GA,features,candidates):
    """Return all the mass difference for each features"""
    mz_diff = []
    idx_feat = []
    mz_ref = []
    unknown_label = len(features)
    for nn in range(len(features)):
        mz_feat = features.mz()[nn]
        if len(GA[nn])>1:
            for snn in GA[nn]:
                if snn==unknown_label:
                    continue
                mz_cand = candidates[snn-unknown_label-1].mass
                mz_diff.append(mz_cand-mz_feat)
                mz_ref.append(mz_feat)
                idx_feat.append(nn)
    return np.abs(np.array(mz_diff)),np.array(idx_feat),np.array(mz_ref)

def get_mass_diff_GA(GA,features,candidates,key='prior_mz'):
    """Return all the mass difference for each features"""
    mz_diff = []
    mz_ref = []
    idx_feat = []
    unknown_label = len(features)
    for nn in range(len(features)):
        mz_feat = features.mz()[nn]
        if len(GA[nn])>1:
            for snn in GA[nn]:
                if snn==unknown_label:
                    continue
                mz_cand = GA[nn][snn][key]
                mz_diff.append(mz_cand)
                mz_ref.append(mz_feat)
                idx_feat.append(nn)
    return np.abs(np.array(mz_diff)),np.array(idx_feat),np.array(mz_ref)
