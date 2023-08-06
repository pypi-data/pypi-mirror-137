from __future__ import annotations
import networkx as nx
import numpy as np
import logging
from simba.annotation.generic.candidate_link import CandidatesLinks
from simba.utils.lsh import LSH
from typing import Optional,List
from simba.io.gem import build_gem_graph
from simba.annotation import scoring



class GemLinks(CandidatesLinks):
    """A class which handles the links related to a biological network, downloaded from the BiGG"""
    def __init__(self, bigg_id:str="Recon3D", scorer:Optional[scoring.DiscreteScorer]=None):
        """[summary]

        Args:
            bigg_id (str, optional): A BiGG (see http://bigg.ucsd.edu/id) id, the model will be downloaded, or parsed if 
            the given id is a valid path. Defaults to None. The parsing only happened at runtime.
            scorer (Optional[scoring.DiscreteScorer], optional): A DiscreteScorer object, to handle scorer. Defaults to None means
            that a sigmoid scorer will be used.

        Raises:
            ValueError: [description]
        """
        self.bigg_id = bigg_id
        super().__init__(scorer=scorer)

    
    def _get_gem_graph(self):
        """"""
        return build_gem_graph(self.bigg_id)

    def initialize(self, annotation) -> GemLinks:
        """Initialize GemLinks object, downloading and parsing the model if necessary.

        Args:
            annotation ([type]): A SimAnnotator object, used to match the GEM metabolites to the candidates.

        Returns:
            GemLinks: The initalized GemLinks object.
        """
        ###This actually perform the computation
        inchikeys,G = self._get_gem_graph()
        candidates = annotation.candidates
        logging.info("Initializing biological links.")
        self.adduct_idx = candidates.adduct_idx
        self.active_count = np.zeros((len(candidates),),dtype=np.int8)
        self.feature_dependent = False

        #We map the ids
        cand_inchikeys = {mol.id:idx for idx,mol in enumerate(candidates.mols)}
        to_delete = [idx for idx,ikey in enumerate(inchikeys) if ikey not in cand_inchikeys]
        G.remove_nodes_from(to_delete)
        new_mapping = {idx:cand_inchikeys[ikey] for idx,ikey in enumerate(inchikeys) if ikey in cand_inchikeys}
        G = nx.relabel_nodes(G, new_mapping,copy=True)
        self.graph = G

        #Saving the unknown label
        self.unknown_label = annotation.unknown_label-len(annotation.features)-1
        self.num_features = annotation.num_features
        return super().initialize(annotation)

    def neighbours(self,node:int) -> List[int]:
        """Return the cnadidtaes ids of the neighbouring candidates given a candidates id."""
        if node==self.unknown_label: return []
        if self.adduct_idx[node] not in self.graph: return []
        return list(self.graph[self.adduct_idx[node]].keys())

