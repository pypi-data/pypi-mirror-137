from abc import ABC,abstractmethod
import networkx as nx
from typing import List,Tuple,Optional
from simba.annotation.features import MsFeatures
from simba.annotation.candidates import CandidatesA
from simba.utils.chunks import chunks
import inspect

class PriorMatch(ABC):
    """This class model the initial matching between a probability and a dataset"""
    def initialize(self,features:MsFeatures,candidates:CandidatesA):
        self.features = features
        self.candidates = candidates
        self.unknown = len(self.features)

    @classmethod
    def args(cls):
        return inspect.signature(cls.__init__)

    def complete_prob_matches(self,GA:nx.Graph,edges:Optional[List[Tuple[int]]] = None, by_batch:int = 10000):
        """Compute the initial probablity of a matching between a fature and a candidates on graph GA.

        Args:
            GA (nx.Graph): The matching graph.
        """
        unknown = self.features.unknown_idx()
        if edges is None:
            edges = list([(e[0],e[1]-unknown-1) for e in GA.edges() if e[0]!=unknown and e[1] != unknown])
        chunks_gen = chunks(edges,by_batch)
        probs = []
        for batch in chunks_gen:
            feats,cands = zip(*batch)
            probs.extend(self.prob_matches(feats,cands))
        return probs

    @abstractmethod
    def prob_matches(self,feats:List[int],cands:List[int]) -> list:
        pass

    @abstractmethod
    def get_unknown_probability(self):
        pass



