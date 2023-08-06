import numpy as np
import logging
from simba.annotation.generic.abstract_link import AnnotationLink
from simba.annotation import scoring
from simba.utils.lsh import LSH

"""
This module store the candidates links. Mandatory (inherited function) are:
    # def initialize(self,self,annot):
    # def get_probs(self,feat,cands,annotation):
    # def update_annotation(self,feat,old_annot,new_annot):
    # def unknown_prob(self):
"""

class CandidatesLinks(AnnotationLink):
    """
    Link whgich can be modelled by counting the connection between links.
    """
    def __init__(self, scorer = None):
        if scorer is None:
            logging.info("No scorer provided, sigmoid scorer used.")
            scorer = scoring.build_sigmoid()
        self.scorer = scoring.DiscreteScorer(fun=scorer,val_max=5000)

    #Can be the annotation object or
    def initialize(self,annot):
        GA = annot.GA
        rfeat = annot._features_iter()
        self.num_features = annot.num_features
        unknown_label = annot.unknown_label-len(annot.features)
        has_adduct = False
        self.active_count = np.zeros((len(annot.candidates),),dtype=np.int8)
        if hasattr(self,'adduct_idx'):
            has_adduct = True

        for ifeat in rfeat:
            icand = GA.nodes[ifeat]["annotation"]-self.num_features-1
            if icand==unknown_label: continue
            for nn in self.neighbours(icand):
                if has_adduct:
                    self.active_count[self.adduct_idx[nn]] += 1
                else:
                    self.active_count[nn] += 1


    def neighbours(self,node):
        """ Return the nighbours of a candidates. Implementation is application dependent"""
        pass

    def get_probs(self,feat,cands,annotation):
        return self.scorer(self.count_active_nodes(np.array(cands)))

    def count_active_nodes(self,node):
        return self.active_count[node]

    def update_annotation(self,feat,old_annot,new_annot,old_neighbours=None,new_neighbours=None):
        """The neihgbours of the old annot need to be uncounted and the neighbours of the new ones are increased"""
        old_neighbours = self.neighbours(old_annot)
        new_neighbours = self.neighbours(new_annot)
        self.active_count[old_neighbours] = self.active_count[old_neighbours]-1
        self.active_count[new_neighbours] = self.active_count[new_neighbours]+1

    def unknown_prob(self):
        return self.scorer(0)

