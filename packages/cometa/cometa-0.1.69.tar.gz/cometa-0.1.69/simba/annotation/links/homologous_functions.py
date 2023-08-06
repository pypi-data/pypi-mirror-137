# Use the non target package to perform implementation
from collections import Counter
import simba.annotation.features as saf
import pandas as pd
import numpy as np

try:
    RPY_PRESENT = True
    from rpy2 import robjects
    import rpy2.robjects.packages as rpackages
    from rpy2.robjects import pandas2ri
    from rpy2.robjects.conversion import localconverter
    from rpy2.rinterface import baseenv,endr
except ModuleNotFoundError:
    RPY_PRESENT = False
    print("Module 'rpy2' is not found.")
##For test

def make_nontarget_table(msfeatures):
    return pd.DataFrame({
    "mass": msfeatures.mz(),
    "intensity":msfeatures.mean_intensity(),
    "rt":msfeatures.rt()
    })


def no_save_cleanup(saveact, status, runlast):
    # cancel all attempts to quit R programmatically
    return 0

#Return the hologuous series as a list of list
# TODO: Handle arguments
def compute_homologuous_cluster(msf,**kwargs):
    # THis is the arguments
    # ['peaklist',
    #  'elements',
    #  'use_C',
    #  'minmz',
    #  'maxmz',
    #  'minrt',
    #  'maxrt',
    #  'ppm',
    #  'mztol',
    #  'rttol',
    #  'minlength',
    #  'mzfilter',
    #  'vec_size',
    #  'mat_size',
    #  'R2',
    #  'spar',
    #  'plotit',
    #  'deb']
    if RPY_PRESENT:
        mnt= make_nontarget_table(msf)
        nontarget = rpackages.importr('nontarget')
        homol_fun = robjects.r['homol.search']
        robjects.r('''
        data(isotopes)
        ''')
        rquit = baseenv['q']
        cleanup = no_save_cleanup
        with localconverter(robjects.default_converter + pandas2ri.converter):
            try:
                res = homol_fun(mnt,robjects.r["isotopes"],**kwargs)
            except Exception as e:
                ERROR_STRING = "no series detected"
                ERROR_STRING2 = "No homologue series detected"
                err_msg = str(e)
                # if ERROR_STRING in err_msg or ERROR_STRING2 in err_msg:
                endr(0)
                return []

        ##The information are in slot 4
        clusters = [None]*len(res[4])
        for idx,elem in enumerate(res[4]):
            cluster = np.array(elem).astype(int).flatten()
            cluster = cluster-1
            cluster=cluster.tolist()
            clusters[idx] = list(set(cluster))
        return clusters
    else:
        return []


def get_formula_counter(smol):
    return Counter([atom.GetSymbol() for atom in smol.mol.GetAtoms()])

def is_subformula(sub_mol,mol):
    csub = get_formula_counter(sub_mol)
    cmol = get_formula_counter(mol)
    cmol.subtract(csub)
    return not any([val<0 for val in cmol.values()])




if __name__ == "__main__":
    import pandas as pd
    PATH_FEATURES = "/home/dalexis/Documents/dev/LCMSBiolGen/data/processed/EcolK12Metabolites_full_lcms.csv"
    features = pd.read_csv(PATH_FEATURES,index_col=False)
    import numpy.random
    import numpy

    NSUPP = 10
    sim_int = numpy.random.uniform(-0.05,1,(features.shape[0],NSUPP))
    sim_int[sim_int<0] = numpy.nan
    for idx in range(NSUPP):
        fname = "Intensity_"+str(idx+1)
        features[fname]=sim_int[:,idx]

    msf = saf.MsFeatures(features)

    import matplotlib.pyplot as plt
    plt.scatter(features.rt,features.mz)

##We add a fake isotopis Series
    mz_earl = 200.1
    rt_earl = 2.5
    rt_shift = 1
    CH2_mass = 14.015650
    import numpy as np
    smass = mz_earl + np.arange(5)*CH2_mass
    srt = rt_earl + np.arange(5)*rt_shift
    mnt= make_nontarget_table(msf)
    mnt.intensity = 10000*mnt.intensity
    vint = np.mean(mnt.intensity)

    supp_df = pd.DataFrame({
    "mass": smass,
    "intensity":vint,
    "rt":srt
    })
    mnt = pd.concat([mnt.reset_index(drop=True), supp_df], axis=0)
    mnt+supp_df
