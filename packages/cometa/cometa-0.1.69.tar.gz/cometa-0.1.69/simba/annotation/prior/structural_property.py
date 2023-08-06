import logging
from abc import ABC,abstractmethod
from simba.entities.representation import RepresentationsDB
import numpy as np
import simba.constants as CONST
from simba.entities.molecule import sibMol
from simba.utils import distributions, matching
from simba.utils.build_fingerprints import build_dense_matrix_from_fingerprints
from simba.annotation.generic.prior_match import PriorMatch
import numpy as np
#THis import is just used for msoothing

from scipy.stats import gaussian_kde
def matching_properties():
    return({
    "mz":"Match using the mass",
    "rt":"Match using the retention time prediction"
    })

def get_property(name):
    name = name.lower()
    link = {"mass":MassProperty,
    "mz":MassProperty,
    "monoisotopic.mass":MassProperty,
    "rt":RtProperty,
    "rtime":RtProperty,
    "retention.time":RtProperty,
    "time":RtProperty,

    }
    ratio,key = matching.match_string(name,list(link.keys()))
    if ratio<0.5:
        raise ValueError("Unknown key :"+name)
    if key!=name:
        logging.warning("Unknown key:"+name+" closest match used is:"+key)
    return link[key]




# class PriorMatch(ABC):
#     def initialize(self,features:MsFeatures,candidates:CandidatesA)
        # self.features = features
        # self.candidates = candidates
#     def prob_matches(self,GA:nx.Graph,by_batch = 10000)
#     def prob_matches(self,feats:List[int],cands:List[int])

###A structural property has two function,
###One which given a structure compute the estimates
class StructuralProperty(PriorMatch,ABC):
    def __init__(self,name,sigma,unknown=2, distribution="gauss"):
        self.dist = distributions.get_distribution(distribution,sigma = sigma)
        self.name = name
        self.unknown_prob = self.dist.pdf(unknown*sigma)/self.dist.pdf(0)
        self.unknown_label = None

    def prob_matches(self,feats,cands):
        feats_vals = self.compute_features(feats)
        cands_vals = self.compute_candidates(cands)
        return self.dist.pdf(cands_vals-feats_vals)/self.dist.pdf(0)

    #Only instantiate if necessary
    def compute_candidate(self,cand):
        pass

    def compute_candidates(self,cands):
        return np.array([self.compute_candidate(self.candidates[cand]) for cand in cands])

    #Onlyu instantiate if necessary
    def compute_feature(self,feat):
        pass

    def compute_features(self,feats):
        return np.array([self.compute_feature(self.features[feat]) for feat in feats])

    def get_unknown_probability(self):
        return self.unknown_prob
    # def computeProbability(self,mol,value):
    #     return self.dist.pdf(value-self.compute(mol))/self.dist.pdf(0)

    # def computeProbabilitiesFromProperties(self,properties,values):
    #     return self.dist.pdf(values-properties)/self.dist.pdf(0)

    # def computeProbabilities(self,mols,values):
    #     properties = self.computeBatch(mols)
    #     self.computeProbabilitiesFromProperties(properties,values)



class MassProperty(StructuralProperty):
    def __init__(self,sigma=None,**kwargs):
        if sigma is None:
            sigma = 0.005
        super(MassProperty, self).__init__(CONST.struct_prop_mass,sigma, distribution = "gaussian")

    def compute_candidate(self,cand):
        return cand.monoisotopic_mass()

    #Onlyu instantiate if necessary
    def compute_features(self,feats):
        return self.features.mz()[np.array(feats)]

###Rt property is dependent of a retention time prediction model
class RtProperty(StructuralProperty):
    def __init__(self,representation:RepresentationsDB,max_rt:float,model=None,descriptor:str=None,relative_deviation:float=0.05):

        self.model=model
        self.representation=representation
        if descriptor is None:
            self.descriptor = CONST.image_desc_name
        else:
            self.descriptor = descriptor
        self.max_rt = max_rt
        self.sigma = relative_deviation/self.max_rt 
        super(RtProperty, self).__init__(CONST.struct_prop_rt,self.sigma, distribution = "t")
        #THe unknown should be close ot the border
        self.unknown = self.dist.pdf(-4)/self.dist.pdf(0)

    def compute_candidates(self, cands):
        mols = [self.candidates[idx] for idx in cands]
        descs = [self.representation[mol,self.descriptor] for mol in mols]
        if self.descriptor == CONST.image_desc_name:
            descs = np.stack(descs)
        else:
            #Fingerprint smaxiumu number of bits
            size_fingerprints = len(self.representation.representations_index[self.descriptor])
            descs = build_dense_matrix_from_fingerprints(descs,size_fingerprints)
        return self.model.predict(descs)


    def compute_features(self, feats):
        return self.features.rt()[np.array(feats)]






class ThresholdedRtProperty(RtProperty):
    """The thresolded RT property add a detection of the problematic beginning and end of the gradient"""
    def __init__(self,begin_interval=0.1,end_interval=0.1,smoothing=0.1,**kwargs):

        super(ThresholdedRtProperty, self).__init__(**kwargs)
        self.begin_interval = begin_interval
        self.end_interval = end_interval
        self.thresh_prob = self.dist.pdf(self.sigma)/self.dist.pdf(0)
        self.smoothing = smoothing
        self.left_bound=0.0
        self.right_bound=0.0


    #THis has an initialisation function
    def initialize(self,features,candidates):
        super(ThresholdedRtProperty, self).initialize(features,candidates)
        self.find_borders()
        logging.info("Rt boundaries detected, peaks falling outside of the interval {{:10.1f}}-{{:10.1f}} will be discarded.".format(self.left_bound,self.right_bound))

    def find_borders(self):
        """Smooth the data and ifnd the beginning and the end of the data using CWT"""
        #max_rt is inherited form RtProperty
        vrt = self.features.rt()/self.max_rt
        kernel = gaussian_kde(vrt,bw_method=self.smoothing)
        xax = np.linspace(0,1,num=200)
        vestimate = kernel(xax)
        idx = 0
        while vestimate[idx]<vestimate[idx+1]:
            idx += 1
        while vestimate[idx+1]<vestimate[idx]:
            idx += 1
        left_bound = idx
        #We set up the right bond
        idx = len(vestimate)-1
        while vestimate[idx]<vestimate[idx-1]:
            idx -= 1
        while vestimate[idx-1]<vestimate[idx]:
            idx -= 1
        right_bound = idx
        self.left_bound = xax[left_bound]*self.max_rt
        self.right_bound = xax[right_bound]*self.max_rt

    def prob_matches(self,feats,cands):
        """This is the only meaningful modification. If the feature fall outside of these bounds we can't use the RT"""
        feats_vals = self.compute_features(feats)
        val_probs = np.repeat(self.thresh_prob,len(feats))
        #We ony compute RT for vraibles which are in the middle of the gradient.
        to_compute = (feats_vals>self.left_bound) & (feats_vals<self.left_bound)
        to_compute = np.where(to_compute)[0]
        if len(to_compute)==0:
            return val_probs
        cand_vals = self.compute_candidates([cands[cc] for cc in to_compute])
        val_probs[np.array(cand_vals)] = self.dist.pdf(cand_vals-feats_vals[to_compute])/self.dist.pdf(0)
        return val_probs

