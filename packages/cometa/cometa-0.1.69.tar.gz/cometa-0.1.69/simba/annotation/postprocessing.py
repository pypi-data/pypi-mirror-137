from simba.annotation.prior.ms2 import MS2Links
from simba.annotation.annotator import SimAnnotator
from simba.annotation.generic.prior_match import PriorMatch
import numpy as np

def get_postprocessor(prior:PriorMatch):
    if isinstance(prior,MS2Links):
        return ReferencesAnnotation()
    return None

class PostProcessing:
    def __init__(self) -> None:
        pass

def format_output(score,name,decimal=3):
    float_formatter = ("{:."+str(decimal)+"f}").format
    return name+"("+float_formatter(score)+")"

class ReferencesAnnotation(PostProcessing):
    """Add the references annotations (ie MS2 or added standard) to the table"""
    def __init__(self,) -> None:
        super().__init__()
    def build_supplementary(self,ms2:MS2Links,annotator:SimAnnotator):
        """This function will return dictionnary of the column to add to the final table"""
        features=annotator.features
        candidates =annotator.candidates
        sname = ms2.name
        supp = [None]*len(features)
        for ifeat in range(len(features)):
            if ifeat not in ms2.mapped_spectra or len(ms2.mapped_spectra[ifeat])==0:
                continue
            else:
                cur_cands = ms2.mapped_spectra[ifeat]
                cands = np.array(list(cur_cands.keys()))
                scores = np.array(list(cur_cands.values()))
                pmax = np.argmax(scores)
                sel_cand = cands[pmax]
                sel_score = scores[pmax]
                ssname = candidates[sel_cand].get_id()
                supp[ifeat] = format_output(sel_score,ssname)

        supp_dic = {sname:supp}
        return supp_dic