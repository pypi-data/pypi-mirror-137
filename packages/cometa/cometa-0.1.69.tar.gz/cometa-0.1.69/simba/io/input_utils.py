import pandas as pd
from simba.entities.adduct import AdductsTree,make_default_adducts
from simba.utils.matching import match_mz
import numpy as np
from simba.annotation.features import MsFeatures
from simba import constants as CONST
from typing import Optional,List,Union

def filter_candidates(mfeatures:MsFeatures,table_candidates:pd.DataFrame,mass_column:str,polarity:Union[str,int]="positive",adducts:Optional[List[str]]=None,ppm:float=10,dmz:float=0.007) -> pd.DataFrame:
    """Filter a table of candidaes to keep only the ones potentially matching a features with their main adducts
    Args:
        mfeatures (MsFeatures): The "MsFeatures" object to filter.
        table_candidates (pd.DataFrame): A pandas DataFrame to filter.
        mass_column (str): The name of the mass column in the table_candidates
        polarity (Union[str,int], optional): The polarity to generate the adducts for. Defaults to "positive".
        adducts (Optional[List[str]], optional): A list of the adducts given as strings. Defaults to None.
        ppm (float, optional): The number of ppm deviations. Defaults to 10.
        dmz (float, optional): The mass deviations in ppm. Defaults to 0.007.

    Returns:
        [type]: [description]
    """
    polarity = CONST.parse_polarity(polarity)
    mcands = table_candidates[mass_column]
    if adducts is None:
        main_add,_ = make_default_adducts(polarity)
    else:
        main_add = adducts

    atree = AdductsTree(main_add,main_add)
    mdiffs,nums,charges = atree.mass_modifications()

    #We compute all the possible masses
    all_masses = []
    for idx in range(len(mdiffs)):
        all_masses.append((nums[idx]*mcands+mdiffs[idx])/(charges[idx]))
    all_masses = np.concatenate(all_masses)

    # We check if at least on mass is in the measured mass range
    measured_mzs = mfeatures.mz_range()
    out_of_bound = (measured_mzs[0]>all_masses)&(measured_mzs[1]<all_masses)
    out_of_bound = out_of_bound.reshape(len(nums),len(mcands))
    out_of_bound = np.where(np.apply_along_axis(all,arr=out_of_bound,axis=0))[0]
    #We generate the mass
    midx = match_mz(mfeatures.mz(),all_masses,ppm = ppm, dmz = dmz)
    sel_cands = set([])
    for mm in midx:
        if mm is None:
            continue
        for e in mm:
            te = e%len(mcands)
            sel_cands.add(te)

    #We add all the out of bound molecules
    [sel_cands.add(x) for x in out_of_bound]
    sel_cands = sorted(list(sel_cands))
    return table_candidates.iloc[sel_cands]


if __name__=="__main__":

    PATH_HMDB = "/home/dalexis/Documents/data/databases/HMDB/hmdb.csv"
    PATH_NIST_ACQUISITION = "/home/dalexis/Documents/data/SRM_NIST_data/processed/datamatrices/annotated_peaktable_8239e4b3d457b2aed8e3418bc684b5e3_full.csv"

    phm = pd.read_csv(PATH_HMDB)
    features = pd.read_csv(PATH_NIST_ACQUISITION,sep="\t")
    mfeatures = MsFeatures(features)

    ###You need to create an adduct tr
    tcandidates = filter_candidates(mfeatures,phm,'exact_mass')
