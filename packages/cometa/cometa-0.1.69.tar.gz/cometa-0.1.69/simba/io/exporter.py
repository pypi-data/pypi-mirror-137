from functools import reduce
from simba.annotation.annotator import get_clusters_simple
from simba.io.samples_parser import load_folder
import numpy as np
import logging
from typing import List,Optional
from simba.annotation.postprocessing import get_postprocessor
from simba.annotation.annotator import SimAnnotator
from simba.io.samples_parser import load_folder


def create_output(probs,names,decimal=3,separator="|",field_separator="::"):
    float_formatter = ("{:."+str(decimal)+"f}").format
    main_name = names[0]
    main_prob = probs[0]
    majority = main_prob>0.5
    full_annot = separator.join([name+field_separator+float_formatter(prob) for name,prob in zip(names,probs)])
    return (main_name,main_prob,majority,full_annot)

#TODO should be a class
def build_table(folder:str,col_ids:List[str]=["name"],max_cand:int = 5,decimal:int=3,
                supp_infos:bool=True,separator:str="|",field_separator:str=";",annotator:Optional[SimAnnotator]=None):

    if supp_infos:
        if annotator is None:
            raise ValueError("annotator must be provided if 'supp_infos' is required")

    LAB_UNKNOWN = "UNKNOWN"
    MAX_VAL = 10000
    sh,features,candidates,GA = load_folder(folder)
    ###We redo the clustrering
    unknown_label = len(features)+1
    vclusters = get_clusters_simple(GA,features,unknown_label)
    dsamples = sh.get_samples_dictionnary(list(range(len(features))))
    fmz = features.mz().tolist()
    frt =  features.rt().tolist()
    main_annots = [None]*len(fmz)
    main_probs = [None]*len(fmz)
    majorities = [None]*len(fmz)
    full_annots = [None]*len(fmz)
    clusters = np.zeros(len(fmz))
    for clust_idx,(ffs,ccs) in enumerate(vclusters):
        for ff in ffs:
            clusters[ff] = clust_idx

            # idx = 1010
    for idx in range(len(dsamples)):
        fsamples = dsamples[idx]
        fsamples
        cands = np.array([cand-len(features)-1 for cand in fsamples.keys()])
        probs = np.array([count for count in fsamples.values()])
        probs = probs/np.sum(probs)
        porder = np.argsort(-probs)
        cands = cands[porder]
        probs = probs[porder]

        if len(cands)>max_cand:
            cands = cands[0:max_cand]
            probs = probs[0:max_cand]
        def build_info(col_ids,cc,fs):
            return fs.join([candidates[int(cc)].get_id()]+[candidates.get_info(col_id,int(cc)) for col_id in col_ids])
        vnames = [build_info(col_ids,int(cc),field_separator)+"("+str(candidates[cc].adduct)+")" if cc!=-1 else LAB_UNKNOWN for cc in cands]
        (main_name,main_prob,majority,full_annot) = create_output(probs,vnames,decimal=decimal,separator=separator,field_separator=field_separator)
        main_annots[idx] = main_name
        main_probs[idx] = main_prob
        if len(cands)>1:
            majorities[idx] = main_prob/(probs[1])
        else:
            majorities[idx] = MAX_VAL
        full_annots[idx] = full_annot

    new_features = features.features.copy()
    new_features["annotation_cluster"]=clusters
    new_features["main_annotation"]=main_annots
    new_features["main_probability"]=main_probs
    new_features["odd_ratio"]=majorities
    new_features["full_annots"]=full_annots

    ##We add the supplementary informations
    if supp_infos:
        posts = [get_postprocessor(prior) for prior in annotator.priors]
        supp_cols = [post.build_supplementary(prior,annotator) for post,prior in zip(posts,annotator.priors) if post is not None]
        supp_cols = reduce(lambda x,y:x.update(y),supp_cols)
        for name,col in supp_cols.items():
            new_features[name]=col
        logging.info("Supplementary columns added {}".format(supp_cols.keys())) 

    return new_features