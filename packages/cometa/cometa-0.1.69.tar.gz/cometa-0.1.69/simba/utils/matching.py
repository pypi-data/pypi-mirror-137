import numpy as np
import difflib
from scipy.spatial import KDTree

def match_mz(x,y,ppm=10,dmz=0.01,single_match=False):
    ox = np.argsort(x)
    oy = np.argsort(y)
    ty = y[oy]
    x_max_ppm = x[ox]+(ppm*x[ox]*1e-6)
    x_max_dmz = x[ox]+dmz
    x_max = np.maximum(x_max_ppm,x_max_dmz)
    x_min_ppm = x[ox]-(ppm*x[ox]*1e-6)
    x_min_dmz = x[ox]-dmz
    x_min = np.minimum(x_min_ppm,x_min_dmz)
    lb = np.searchsorted(ty,x_min)
    ub = np.searchsorted(ty,x_max)

    size_matches = ub-lb
    res = [None] * ox.shape[0]
    for idx in range(len(res)):
        if size_matches[idx]==0: continue
        val_idx = oy[lb[idx]:ub[idx]]
        res[ox[idx]]=list(val_idx)

    return res

def match_string(string,strings):
    ratios = [difflib.SequenceMatcher(None, string, x).ratio() for x in strings]
    sel_key = [string for string,ratio in zip(strings,ratios) if ratio==max(ratios)]
    return max(ratios),sel_key[0]

def match_precursor(mzf,rtf,mzo,rto,mztol=0.007,rttol=5):
    def format_infos_kdtree(vals):
        if isinstance(vals,list):
            vals = np.array(vals)
            vals = vals[:,np.newaxis]
        else:
            if not isinstance(vals,np.ndarray):
                vals = np.array(vals)
            if len(vals.shape)==1:
                vals = vals[:,np.newaxis]
        return vals

    mzf = format_infos_kdtree(mzf)
    rtf = format_infos_kdtree(rtf)
    mzo = format_infos_kdtree(mzo)
    rto = format_infos_kdtree(rto)
    fcoords = np.hstack([mzf/mztol,rtf/rttol])
    ocoords = np.hstack([mzo/mztol,rto/rttol])
    fktree = KDTree(ocoords)
    closest = fktree.query(fcoords,k=1)[1]
    return closest

class MS2Links:
    def __init__(self,ms2_annotation):
        if not isinstance(ms2_annotation,pd.DataFrame):
            ms2_annotation = pd.read_csv(ms2_annotation, delimiter = '\t')
        mz,rt,score,inchikey,inchi = self.parse_ms2_annotation(ms2_annotation)
        self._mz_prec = mz
        self._rt_prec = rt
        self._inchikey = inchikey
        self._inchi = inchi
        self._score = score
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
    def match_precursor(self,features,candidates,mztol=0.007,rttol=5):
        mzo = (self.mz_precursor()[:,np.newaxis])
        rto = (self.rt_precursor()[:,np.newaxis])
        wo = self.match_score()
        inchikeyo = self.inchikey()
        mzf = features.mz().to_numpy()[:,np.newaxis]
        rtf = features.rt().to_numpy()[:,np.newaxis]
        fcoords = np.vstack([mzf/mztol,rtf/rttol])
        ocoords = np.vstack([mzo/mztol,rto/rttol])
        fktree = KDTree(fcoords)
        # We map the inchikey to the inchikey of candidates
        map_id_candidates = {icand:candidates[icand].id for icand in range(len(candidates))}
        mapped_ms2_inchikey = [map_id_candidates[inchikey] if inchikey in map_id_candidates else None for inchikey in inchikeyo]
        #closest neighbours
        closest = fktree.query(ocoords,k=1)
        feat_match = {feat:(we,mapped_ms2_inchikey[imol]) for feat,imol,we in zip(closest,range(mzo.shape[0]),wo.tolist()) if mapped_ms2_inchikey[imol] is not None}
        return feat_match




if __name__=="__main__":
    x =  np.array([ 0. ,  1.2,  7. , 10. , 50. ])
    y = np.array([1. , 2. , 1.2, 3. , 4. , 5. , 9. , 6. , 4. , 7.,7.0005 , 8. ])

    match_mz(x,y)
