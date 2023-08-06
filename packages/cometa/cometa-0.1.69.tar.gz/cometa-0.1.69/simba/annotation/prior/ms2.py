import numpy as np
import pandas as pd
import logging
import os
import glob
from scipy.spatial import KDTree
from simba.entities.molecule import build_sibmols
from scipy.stats import norm
from typing import List, Optional
from simba.annotation.candidates import CandidatesA
from simba.annotation.features import MsFeatures
from simba.annotation.generic.prior_match import PriorMatch
 
def normalize_normal(x):
    temp =  norm(0,np.std(x)).pdf((x-np.mean(x))).tolist()
    return temp/np.sum(temp)


def normalize_exp(x):
    x = np.array(x)
    return (np.exp(-x)/np.sum(np.exp(-x))).tolist()

def normalize_identity(x):
    return x

def get_scaler(name):
    if name=="normal":
        return normalize_normal
    if name=="exp":
        return normalize_exp
    return normalize_identity


def sanitize_inchi(inchi):
    if pd.isnull(inchi): return None
    if inchi.startswith('InChI'):
        return inchi
    if inchi.startswith('"') or inchi.startswith("'"):
        return inchi[1:-1]
    if inchi.startswith('1S'):
        return('InChI')+inchi
    return None

#    def initialize(self,features:MsFeatures,candidates:CandidatesA):
#     def complete_prob_matches(self,GA:nx.Graph,all_edges:Optional[List[Tuple[int]]] = None, by_batch:int = 10000):
#     def prob_matches(self,feats:List[int],cands:List[int]):
#     def get_unknown_probability(self):
class MS2Links(PriorMatch):
    def __init__(self,ms2_annotation:pd.DataFrame,scaler:str='identity',mztol:float=0.005,rttol:float=5,name=None,low_score = 0.5,delimiter="\t"):
        self.name=name
        if os.path.isfile(ms2_annotation):
            ms2_annotation = pd.read_csv(ms2_annotation, delimiter = delimiter)
        self.scaler = get_scaler(scaler)
        self.mztol = mztol
        self.rttol = rttol
        self.low_score = low_score
        logging.info("Parsing MS2 annotation")
        mz,rt,score,inchikey,inchi = self.parse_ms2_annotation(ms2_annotation)
        logging.info("Finished parsing MS2 annotation")
        self._mz_prec = mz
        if max(rt)>100:
            rt = rt/60
        self._rt_prec = rt
        self._inchikey = inchikey
        self._inchi = inchi
        self._score = score
        #The unknown probability is 
        self.compute_unknown()

    def compute_unknown(self):
        #This will always favor MS2 annotation
        self.unknown_prob = min(self._score)*0.75

    def initialize(self, features: MsFeatures, candidates: CandidatesA):
        super().initialize(features, candidates)
        self.mapped_spectra = self.match_precursor()
        logging.info(str(len(self.mapped_spectra))+" MS2 precursor matched.")

    def prob_matches(self,feats:List[int],cands:List[int]):
        #We have match the to the inchikey in the different dataset
        num_ms2 = 0
        scores_ms2 = [self.unknown_prob]*len(feats)
        for idx,(ifeat,icand) in enumerate(zip(feats,cands)):
            if not ifeat in self.mapped_spectra:
                continue
            if icand in self.mapped_spectra[ifeat]:
                scores_ms2[idx] = 1+(self.mapped_spectra[ifeat][icand]-self.low_score)
        return scores_ms2
         
    def get_unknown_probability(self):
        return self.unknown_prob

    def parse_ms2_annotation(self,ms2_annotation):
        pass

    def mz_precursor(self):
        return self._mz_prec

    def rt_precursor(self):
        return self._rt_prec

    def match_score(self):
        return self._score
        
    def inchikey(self):
        return self._inchikey

    def inchi(self):
        return  self._inchi

    def match_precursor(self):
        mzo = (self.mz_precursor()[:,np.newaxis])
        rto = (self.rt_precursor()[:,np.newaxis])
        wo = self.match_score()
        inchikeyo = self.inchikey()
        mzf = self.features.mz().to_numpy()[:,np.newaxis]
        rtf = self.features.rt().to_numpy()[:,np.newaxis]
        if np.max(rto)>np.max(rtf):
            rto = rto/60

        fcoords = np.hstack([mzf/self.mztol,rtf/self.rttol])
        ocoords = np.hstack([mzo/self.mztol,rto/self.rttol])
        fktree = KDTree(fcoords)
        #closest neighbours
        closest = fktree.query(ocoords,k=1)
        # We map the inchikey to the inchikey of candidates
        map_id_candidates = {}
        for icand in range(len(self.candidates)):
            ikey = self.candidates[icand].get_id()
            mass = self.candidates[icand].mass
            if ikey in map_id_candidates:
                map_id_candidates[ikey].append((icand,mass))
            else:
                map_id_candidates[ikey] = [(icand,mass)]

        #map_id_candidates = {icand:self.candidates[icand].id for icand in range(len(self.candidates))}
        def get_true_match(mic,cmz):
            vmin = 1000
            imatch = None
            for icand,imass in mic:
                dmz = abs(cmz-imass)
                if dmz<vmin:
                    vmin = dmz
                    imatch = icand
            return imatch

        mapped_ms2_inchikey = [get_true_match(map_id_candidates[inchikey],cmz) if inchikey in map_id_candidates else None for cmz,inchikey in zip(mzo,inchikeyo)]

        #Authorize multi match
        feat_match = {}
        for feat,imol,we in zip(closest[1],range(mzo.shape[0]),wo.tolist()):
            if mapped_ms2_inchikey[imol] is None:
                continue
            if feat in feat_match:
                feat_match[feat][mapped_ms2_inchikey[imol]]=we
            else:
                feat_match[feat] = {mapped_ms2_inchikey[imol]:we}
        return feat_match
    
    def get_rt_preds_args(self):
        mlist = build_sibmols(self.inchi())
        sel_indexes = [idx for idx,(mol,valid) in enumerate(mlist) if valid]
        sel_mols = [mlist[idx][0] for idx in sel_indexes]
        sel_rts = [self.rts()[idx] for idx in sel_indexes]
        return sel_mols,sel_rts


class MS2LinksCsv(MS2Links):
    def __init__(self,ms2_annotation:str,scaler:str='identity',mztol:float=0.005,rttol:float=5,name=None,low_score = 0.5,
    col_mz_prec:str='mz',col_rt_prec:str='rt',col_score:str="score",col_inchi="inchikey",col_inchikey:Optional[str]=None,**kwargs):
        self.col_mz_prec = col_mz_prec
        self.col_rt_prec = col_rt_prec
        self.col_score = col_score
        self.col_inchi = col_inchi
        self.col_inchikey = col_inchikey
        super().__init__(ms2_annotation,scaler,mztol,rttol,name,low_score,**kwargs)

    def parse_ms2_annotation(self,ms2_annotation):
        logging.info("Parsing MS2 annotation")
        mz = ms2_annotation[self.col_mz_prec].to_numpy()
        rt = ms2_annotation[self.col_rt_prec].to_numpy()
        score = ms2_annotation[self.col_score].to_numpy()
        inchi = ms2_annotation[self.col_inchi].to_list()
        if self.col_inchikey is not None:
            inchikey = ms2_annotation[self.col_inchikey].to_numpy()
        else:
            print("No inchikey column, parsing molecules")
            bmols = build_sibmols(inchi)
            inchikey = [bmol.get_id() for bmol,_ in bmols]
        return mz,rt,score,inchikey,inchi


class GNPSLibraryLinks(MS2Links):
    def __init__(self, ms2_annotation: pd.DataFrame, scaler: str = 'identity', mztol: float = 0.005, rttol: float = 5, low_score=0.5,**kwargs):
        super().__init__(ms2_annotation, scaler=scaler, mztol=mztol, rttol=rttol, low_score=low_score,name="MS2_GNPS",**kwargs)
    def parse_ms2_annotation(self,ms2_annotation:pd.DataFrame):
        """[summary]

        Args:
            ms2_annotation (pd.DataFrame): [description]

        Returns:
            [type]: [description]
        """
        pda = ms2_annotation
        cleaned_inchi = [sanitize_inchi(inchi) for inchi in pda["INCHI"].tolist()]
        valid_inchis = [inchi is not None for inchi in cleaned_inchi]
        pda = pda[valid_inchis]
        inchi = [sanitize_inchi(inchi) for inchi in pda["INCHI"].tolist()]
        inchikey = pda["InChIKey-Planar"].tolist()
        mz = np.array(pda["SpecMZ"].tolist())
        rt = np.array(pda["RT_Query"].tolist())
        score = np.array(pda["MQScore"].tolist())
        return mz,rt,score,inchikey,inchi

class AnnotationFlowLinks(MS2Links):
    def __init__(self, ms2_annotation: pd.DataFrame, scaler: str = 'identity', mztol: float = 0.005, rttol: float = 5, low_score=0.5,**kwargs):
        super().__init__(ms2_annotation, scaler=scaler, mztol=mztol, rttol=rttol, name="MS2_AFLOW", low_score=low_score,**kwargs)
    def parse_ms2_annotation(self,ms2_annotation:pd.DataFrame,selected_source:List[str] = ["nist","lipidmaps"]):
        pda = ms2_annotation
        pda = pda[pda["identification_method"]=="[annotate_db:ms2]"]
        pda = pda[pda["inchi"].notna()]
        pda = pda[pda["inchi"]!=" "]
        inchi = pda["inchi"].tolist()
        inchikey = [x[0:14] for x in pda["opt_global_inchikey"].tolist()]
        mz = np.array(pda["exp_mass_to_charge"].tolist())
        rt = np.array(pda["opt_global_experimental_retention_time"].tolist())
        score = np.array(pda["id_confidence_measure[ms2_score]"].tolist())
        return mz,rt,score,inchikey,inchi

def process_sirius_dir(pdir,scaler):
    default_df = pd.DataFrame({'mz':[],'rt':[],'score':[],'inchikey':[],'inchi':[]})
    pfid = os.path.join(pdir,'fingerid')
    pinfo = os.path.join(pdir,'compound.info')
    tab_info = pd.read_csv(pinfo,delimiter="\t")
    vmz = float(tab_info.iloc[1,1])
    vrt = tab_info.iloc[tab_info['index'].tolist().index('rt'),1]
    vrt = float(vrt.split(":")[0])
    inchikey = []
    score = []
    inchi = []
    if os.path.isdir(pfid):
        #Mass and retention time
        for x in glob.glob(os.path.join(pfid,"*.tsv")):
            finfos = pd.read_csv(x,delimiter = "\t")
            if finfos.shape[0]==0:
                continue
            inchikey.extend(finfos.inchikey2D.tolist())
            inchi.extend(finfos.inchi.tolist())
            ##WE have to nromalize the score.
            vscore = finfos.score.tolist()
            vscore = scaler(vscore)
            score.extend(vscore)
    else:
        return default_df
    mz = [vmz]*len(inchi)
    rt = [vrt]*len(inchi)
    return pd.DataFrame({"mz":mz,"rt":rt,"score":score,"inchikey":inchikey,"inchi":inchi})

def is_valid_sirius(path_dir):
    cinfo = os.path.join(path_dir,"compound.info")
    cms = os.path.join(path_dir,"spectrum.ms")
    if not os.path.isfile(cinfo) and not os.path.isfile(cms):
        return False
    return True

class SiriusLink(MS2Links):
    def __init__(self, ms2_annotation:str, scaler="normal"):
        """Compute prior annotation using SIRIUS data.

        Args:
            ms2_annotation (str): A path to a SIRIUS folder.
            scaler (str, optional): The name of a scaler used to normalize CSI:FingerID score, shoud be 'normal' or 'exp'. Defaults to 'normal'.

        Raises:
            FileNotFoundError: [description]
        """
        if not os.path.isdir(ms2_annotation):
            raise FileNotFoundError("SIRIUS workspace directory "+ms2_annotation+" does not exists")
        super().__init__(ms2_annotation, scaler=scaler, name="MS2_SIRIUS")

    def parse_ms2_annotation(self, ms2_annotation):
        logging.info('Beginning the parsing of SIRIUS data')
        ##The MS2 annotation is a folder
        dir_spectra = [os.path.join(ms2_annotation,folder) for folder in os.listdir(ms2_annotation)]
        all_matches = []
        for res_dir in dir_spectra:
            if is_valid_sirius(res_dir):
                vpro = process_sirius_dir(res_dir,self.scaler)
                all_matches.append(vpro)
        rval = pd.concat(all_matches)
        return (rval.mz.tolist(),rval.rt.tolist(),
        rval.score.tolist(),rval.inchikey.tolist(),
        rval.inchi.tolist())