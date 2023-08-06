import networkx as nx
import numpy as np
import os
from simba.annotation.generic.abstract_link import AnnotationLink
from simba.utils.matching import match_precursor
from simba.similarities.molecular_similarity import CachedTanimotoSimilarity
from simba.utils.arguments_checking import check_range,check_type

GNPS_RT_NAME = 'precursor mass'
GNPS_MZ_NAME ='RTMean'
GNPS_EDGE_SCORE = 'EdgeScore'
GRAPH_EDGE_SCORE = "s"
MIN_SCORE = 0.5
MIN_PROB = 0.001


#Harmonic mean of the two similarity
def compute_edge_score(sim_mol,edge_score):
    return ((1+sim_mol)*(1+edge_score))**3

class NetworkMSMSLinks(AnnotationLink):
    def __init__(self,path_gml:str,mztol:float=0.007,rttol:float=5.0):
        """Create an MS-MS network link from a GNPS network.

        Args:
            path_gml (str): The path of the .graphml file computed using GNPS.
            mztol (float, optional): The tolerance to match the mass to the precursors. Defaults to 0.007.
            rttol (float, optional): The tolerance to match the retention time to the precursors. Defaults to 5.0.

        Raises:
            FileNotFoundError: Raised if 'path_gml' is not found.
        """
        #Getting features
        self.path_gml = path_gml
        if not os.path.isfile(path_gml):
            raise FileNotFoundError("File {0} is not found.".format(path_gml))
        ###We randomly sample a number from the rest of the data 
        self.mztol = check_range(mztol,(0.0005,0.1))
        self.rttol = check_type(rttol,float,"rttol")

    def compute_default(self):
        #The default is the minimum similarity.
        all_scores = [dat[GRAPH_EDGE_SCORE] for e1,e2,dat in self.graph.edges(data=True)]
        return min(all_scores),0.5

    def initialize(self,annotation):
        """Initalize the object

        Args:
            annotation (SimAnnotator): A SimAnnotator object, the candidates will be retrieved from it.
        """
        self.features = annotation.features
        self.candidates = annotation.candidates
        self.mol_sim = CachedTanimotoSimilarity(annotation.representations)
        self.min_score = MIN_SCORE
        self.unknown_label = annotation.unknown_label
        self.num_features = len(self.features)

        feat_mz = self.features.mz()
        feat_rt = self.features.rt()

        #Getting the grpahML file
        gml = nx.read_graphml(self.path_gml)
        prec_mz = [gml.nodes[nn]['precursor mass'] for nn in gml.nodes()]
        prec_rt = [gml.nodes[nn]['RTMean'] for nn in gml.nodes()]
        gm_nodes = list(gml.nodes())

        #Return the closest precursor using a kdtree
        vmatch = match_precursor(prec_mz,prec_rt,feat_mz,feat_rt,mztol=self.mztol,rttol=self.rttol)

        #We create the index
        idx_gml = {gm_nodes[iprec]:ifeat for iprec,ifeat in enumerate(vmatch)}

        #We create the relationship graph
        self.graph = nx.Graph()
        self.graph.add_nodes_from(list(range(annotation.num_features)))

        #We add the edges
        all_edges = [(idx_gml[na],idx_gml[nb],{GRAPH_EDGE_SCORE:ndat[GNPS_EDGE_SCORE]}) for na,nb,ndat in gml.edges(data=True)]
        self.graph.add_edges_from(all_edges)

        #We initialize the mean similarity
        self.mean_score = np.zeros(annotation.num_features)
        self.count_features = np.array([len(self.graph[rr]) for rr in range(annotation.num_features)])

        #We compute the default term (To modify)
        self.prob_default = compute_edge_score(*self.compute_default())


    def update_annotation(self,feat,old_annot,new_annot):
        pass

    def get_prob(self,feat,cand,annotation):
        nfeats = list(self.graph[feat].keys())
        if len(nfeats)==0:
            return self.prob_default
        icands = annotation[nfeats]
        ccand = self.candidates[cand]
        #This is an epsilon to avoid 0 cases
        vscore = 0.0001
        for ifeat,keyfeat in enumerate(nfeats):
            icand = icands[ifeat]
            if icand==self.unknown_label:
                vscore += MIN_SCORE
                continue
            micand = self.candidates[icand-self.num_features]
            mol_sim = self.mol_sim.computeSimilarity(ccand,micand)
            edge_sim = self.graph[feat][nfeats[ifeat]][GRAPH_EDGE_SCORE]
            vscore += compute_edge_score(mol_sim,edge_sim)
        return vscore/len(nfeats)

    def get_probs(self,feat,cands,current_annotation):
        probs = np.array([self.get_prob(feat,cand,current_annotation) for cand in cands])
        return probs

    def unknown_prob(self):
        return MIN_SCORE

