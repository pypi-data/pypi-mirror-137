import networkx as nx
import numpy as np
import math
import logging
from simba.annotation.generic.candidate_link import CandidatesLinks
from simba.utils.build_fingerprints import build_dense_matrix_from_fingerprints
import simba.constants as const
from simba.annotation import scoring
import tensorflow.keras as K
from scipy.sparse import vstack
import tqdm
from typing import Optional
from simba.utils.lsh import LSH



def load_model():
    """This function load the chemical similarity embbedding model"""
    path_model = const.path_model_biological
    logging.debug("Loading model from: "+path_model)
    model = K.models.load_model(path_model,compile=False)
    #We rebuild the two first layers
    names = [weight.name for layer in model.layers for weight in layer.weights]
    weights = model.get_weights()
    weights_dic = {}
    for name, weight in zip(names, weights):
        weights_dic[name]=weight

    # TODO: Pass into constant files
    HIDDEN_NEURONE_1 = 512
    HIDDEN_NEURONE_2 = 256
    size_embbedding = 24
    #We create the model for coordinates predictions
    npoint = K.layers.Input(shape=(None,const.size_fingerprint_biological))
    new_hidden_1 = K.layers.Dense(HIDDEN_NEURONE_1,name="new_hidden_1")(npoint)
    new_hidden_2 = K.layers.Dense(HIDDEN_NEURONE_2,name="new_hidden_2")(new_hidden_1)
    new_coords = K.layers.Dense(size_embbedding,name="new_coord")(new_hidden_2)

    # We set the wieghts of the layers
    pred_model = K.models.Model(inputs=npoint,outputs=new_coords)
    pred_model.layers[1].set_weights((weights_dic['point_hidden_1/kernel:0'],weights_dic['point_hidden_1/bias:0']))
    pred_model.layers[2].set_weights((weights_dic['point_hidden_2/kernel:0'],weights_dic['point_hidden_2/bias:0']))
    pred_model.layers[3].set_weights((weights_dic['point_emb/kernel:0'],weights_dic['point_emb/bias:0']))
    return pred_model

# TODO: implement this
class ChemicalSimilarityLinks(CandidatesLinks):
    def __init__(self,scorer:Optional[scoring.DiscreteScorer]=None,epsilon:float=1.0):
        """Create a ChemicalSimilarity approximating ChemicalSImilarity of compounds.

        Args:
            scorer (scoring.DiscreteScorer, optional): A DiscreteScorer object. Defaults to None.
            epsilon (float, optional): The euclidian distance in the threshold. Defaults to 1.0.

        Raises:
            ValueError: Raised if epsilon is too high or too low.
        """
        if epsilon<0.001:
            raise ValueError("Epsilon value of {0} is too low.".format(epsilon))
        if epsilon>10.00:
            raise ValueError("Epsilon value of {0} is too high.".format(epsilon))
        self.epsilon = epsilon
        super().__init__(scorer=scorer)
    
    def initialize(self, annotation):
        """Compute an approximation of chemical similarity using LSH on a set of candidates.

        Args:
            annotation (SimAnnotator): A SimAnnotator object, the candidates will be retrieved from it.

        Returns:
            ChemicalSimilarityLinks: The initalized ChemicalSimilarityLinks object.
        """
        candidates = annotation.candidates
        representation = annotation.representations
        logging.info("Initializing biological links.")
        self.model = load_model()
        self.adduct_idx = candidates.adduct_idx
        self.active_count = np.zeros((len(candidates),),dtype=np.int8)
        self.feature_dependent = False
        #Initializing the fingerprints
        fingerprints = [None]*(candidates.adduct_idx[-1]+1)
        current_mol = -1
        for aidx in range(len(candidates)):

            if candidates.adduct_idx[aidx]==current_mol: continue
            current_mol = candidates.adduct_idx[aidx]
            #We compute the fingerprints
            fingerprints[current_mol] = representation[candidates[aidx],"struct-fingerprints"]
        #We do the predictions by batches
        BATCH_SIZE = 500
        cuts = list(range(0,len(fingerprints),BATCH_SIZE))
        if cuts[-1] != len(fingerprints):
            cuts = cuts+[len(fingerprints)]
        coords = [None]*(len(cuts)-1)
        for bidx in range(len(cuts)-1):
            fmat = build_dense_matrix_from_fingerprints(fingerprints[cuts[bidx]:cuts[bidx+1]],const.size_fingerprint_biological)
            coords[bidx] = self.model.predict(fmat)
        if len(coords)==0:
            coords = coords[0]
        else:
            coords = vstack(coords)
        ndim = coords.shape[1]
        #We unsparse the matrix
        coords = coords.todense()
        #We apply LSH on all the datasets
        vlsh = LSH(math.floor(ndim/3),ndim,windows=self.epsilon*2)
        vlsh.store(coords)
        logging.info("Building chemical similarity neighborhood (This is the time consuming step)")
        ##Non parallel version
        neighbours = vlsh.nn_radius_points(coords,self.epsilon)
        self.graph = nx.Graph()

        #We intialize all the nodes
        self.graph.add_nodes_from(list(range(len(neighbours))))

        ##We add all the ocmputed neighbours
        for idx in tqdm.tqdm(range(len(neighbours))):
            tedges = [(idx,nn) for nn in neighbours[idx] if idx!=nn]
            self.graph.add_edges_from(tedges)

        #Saving the unknown label
        self.unknown_label = len(annotation.features)
        self.num_features = annotation.num_features
        logging.info("Initializing biological similarity.")
        return super().initialize(annotation)

    def neighbours(self,node):
        if node==self.unknown_label: return []
        return list(self.graph[self.adduct_idx[node]].keys())