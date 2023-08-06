import logging
import os
import pickle
import importlib
from collections import Counter

import networkx as nx
import numpy as np
from typing import Union,List,Optional
import tqdm
import itertools

from simba.annotation.generic.abstract_link import AnnotationLink
from simba.annotation.generic.prior_match import PriorMatch
from simba.annotation.candidates import Candidates, CandidatesA
from simba.annotation.features import MsFeatures
from simba.exceptions import RtNotFoundError

from simba.annotation.helper_links import get_link
from simba.annotation.helper_priors import get_prior

from simba.utils.chunks import chunks
from simba.utils.timer import Timer

import simba.constants as CONST
from simba.entities.representation import build_representation,RepresentationsDB
import cython

import isoclustcython

from simba.io.fullstorer import HDF5storer, store_candidates, store_features


#THis is just to handle the visualisation
matplotlib_loader = importlib.find_loader('matplotlib')
MPL_FOUND = matplotlib_loader is not None
if MPL_FOUND:
    import matplotlib.pyplot as plt

TIMER = True

class SimAnnotator:
    """
    Similarity based annotation object
    """
    def __init__(self,features:MsFeatures,candidates:CandidatesA,
    links:Union[List[str],List[AnnotationLink]] = ["bio","homologuous","adduct"],
    priors:Union[List[str],List[PriorMatch]] = ["mz","rt"],storage=Optional[Union[str,RepresentationsDB]]):
        """A similarity based annotation object.

        Parameters
        ----------
        features : MsFeatures
            A set of MS features in a MsFeature object created using the MsFeatures objects.
        candidates : Candidates/CandidatesA
            A set of moelcular structures in a candidates object with adducts information included (CandidatesA)
        storage : A path where the probablistic hdf5 will be stored.
            A directory to store the temnporary files.
        links : List of String or links objects
        todo : The others arguments or maybe refactor

        Returns
        -------
        type
            A SimAnnotator object.

        """

        self.representations = build_representation(storage)

        if not isinstance(features,MsFeatures):
            raise TypeError("'features' should be a MsFeatures object.")

        if not isinstance(candidates,Candidates):
            raise TypeError("'candidates' should be a CandidatesSet object.")
        self.features = features
        self.candidates = candidates

        # Candidates links parsing and initialisation only
        if not isinstance(links,list):
            raise TypeError("'links' should be a list.")
        else:
            self.links = []
            for val in links:
                if isinstance(val,str):
                    supp_args = self.get_init_args(val)
                    to_instantiate = get_link(val)
                    if to_instantiate.__name__ != "AdductLinks":
                        logging.warning("The link provided is a string '{0}', it is recommended to instantiate the link for fine control of parameters.".format(val))
                    self.links.append(to_instantiate(**supp_args))
                elif isinstance(val, AnnotationLink):
                    self.links.append(val)
                else:
                    raise ValueError("All 'links' elements should be 'str' or 'AnnotationLink'")

        # Candidates priors parsing and initialisation only
        if not isinstance(priors,list):
            raise TypeError("'priors' should be a list.")
        else:
            self.priors = []
            for val in priors:
                if isinstance(val,str):
                    supp_args = self.get_init_args(val)
                    to_instantiate = get_prior(val)
                    logging.warning("The priors provided is a string '{0}', it is recommended to instantiate the prior for fine control of parameters.".format(val))
                    self.priors.append(to_instantiate(**supp_args))
                elif isinstance(val, PriorMatch):
                    self.priors.append(val)
                else:
                    raise ValueError("All 'priors' elements should be 'str' or 'PriorMatch'")
        
        #We check if the RtProperty is saved
        rt_class = get_prior("rt")
        self.rt_property = None
        for prior in self.priors:
            if isinstance(prior,rt_class):
                self.rt_property = prior
        if self.rt_property is None:
            raise RtNotFoundError("RtProperty not set. SLAW is not runnable without an RtProperty")
        


    # TODO: Implement Features as an expansion mz
    def create_matching(self,ppm=10,dmz=0.002):
        print("Compute the initial matching.")
        matches = [self.candidates.find_masses(mz,ppm=ppm,dmz=dmz)
         for mz in self.features.mz()]
        def build_set_from_matches(matches):
            unique_candidates = set([m for match in \
            matches for m in match])
            return unique_candidates
        acands = build_set_from_matches(matches)
        _ = self.candidates.reduce_candidates(acands)

        #There is always a filtration on the mass
        matches = [self.candidates.find_masses(mz,ppm=ppm,dmz=dmz) for mz in self.features.mz()]
        self.GA = nx.Graph()

        #We add all the nodes
        self.num_features = len(self.features)
        self.num_candidates = len(self.candidates)

        #Unknown metabolites is the total number of features +1
        self.unknown_label = self.features.unknown_idx()
        self.GA.add_nodes_from(list(range(self.num_features+self.num_candidates+1))+[self.unknown_label])

        #We build the annotation graph
        for idx in range(len(matches)):
            edges_to_add = [(idx,match+self.num_features+1) for match in matches[idx]]+[(idx,self.unknown_label)]
            self.GA.add_edges_from(edges_to_add)

        #We add the edges to complete the cluters in every cases
        logging.info("Completing the clusters")
        clusters = get_clusters(self)
        for cluster in clusters:
            self.GA.add_edges_from(list(itertools.product(cluster[0],cluster[1])))

        #COmputing the prior probablity
        self.initialize_priors()
        self.compute_priors()

    def get_init_args(self,link):
        if isinstance(link,str):
            raw_name = link
        else:
            raw_name = link.__name__
        supp_args = {}
        if raw_name=="GemGraph":
            supp_args['bigg_id'] = self.bigg_id
        if raw_name=="NetworkMSMSLink":
            supp_args['path_gml'] = self.path_gnps
        return supp_args

    def initialize_priors(self):
        logging.info("Initializing priors.")
        for prior in self.priors:
            prior.initialize(self.features,self.candidates)
    
    def prior_names(self):
        return [CONST.PRIOR+"_"+prior.__class__.__name__ for prior in self.priors]


    def compute_priors(self):
        logging.info("Computing prior probabilities")
        prior_probabilities = []
        prior_names = self.prior_names()
        self.GA.graph[CONST.PRIOR_SUPP] = prior_names


        unknown_probs = [prior.get_unknown_probability() for prior in self.priors]
        unknown_prob = np.prod(unknown_probs)
        self.GA.graph[CONST.UNKNOWN_PROB] = unknown_prob

        unknown_idx = self.features.unknown_idx()
        all_edges = list([(e[0],e[1]-unknown_idx-1) for e in self.GA.edges() if e[0]!=unknown_idx and e[1] != unknown_idx])
        for prior in self.priors:
            prior_probabilities.append(prior.complete_prob_matches(self.GA,edges=all_edges))

        #Maybe add a mixture
        #We compute the final probability
        prior_probabilities = np.stack(prior_probabilities)
        # final_prior = np.prod(prior_probabilities,axis=1)

        #We add the known probability
        for prior_idx,(e1,e2) in zip(range(prior_probabilities.shape[1]),all_edges):
            current_priors = prior_probabilities[:,prior_idx]
            self.GA[e1][e2+unknown_idx+1][CONST.PRIOR] = np.prod(current_priors)
            self.GA[e1][e2+unknown_idx+1][CONST.PRIOR_SUPP] = current_priors

        #We add the unknown probability
        for ifeat in range(len(self.features)):
            self.GA[ifeat][unknown_idx][CONST.PRIOR] = unknown_prob
            self.GA[ifeat][unknown_idx][CONST.PRIOR_SUPP] = unknown_probs
        

    def _candidates_iter(self):
        return range(self.num_features+1,self.num_features+self.num_candidates+1)

    def _features_iter(self):
        return range(0,self.num_features)

    def prior_annotation(self,seed=512):
        priors = self.compute_prior()
        sel_features = [idx for idx in range(self.num_features) if len(self.GA[idx])>0]

        # Random initial annotation
        def get_prob(graph,node,name=CONST.PRIOR,forbidden_values=set([])):
            gg = graph[node]
            nodes = [ng for ng in gg.keys() if ng not in forbidden_values]
            probs = np.array([gg[ng][name] for ng in nodes])
            return nodes,probs/np.sum(probs)

        #We ensure that the data are correctly sampled correctly.
        already_annotated = set([])
        for feat in sel_features:
            nodes,probs = get_prob(self.GA,feat,CONST.PRIOR,forbidden_values=already_annotated)
            if len(nodes)==1:
                self.GA.nodes[feat]["annotation"]=nodes[0]
            else:
                tannot = np.random.choice(nodes,size=1,p=probs)
                self.GA.nodes[feat]["annotation"]=tannot[0]
            if self.GA.nodes[feat]["annotation"]!=self.unknown_label:
                already_annotated.add(self.GA.nodes[feat]["annotation"])

    def save_GA(self,path):
        with open(path,"wb") as f:
            pickle.dump(self.GA,file=f)


    def save(self,path_folder,create=False,overwrite=False):
        if not os.path.isdir(path_folder):
            if create:
                os.makedirs(path_folder)
            else:
                raise FileNotFoundError("Directory:"+path_folder,"does not exists to create it set create=True")
        else:
            path_candidates=os.path.join(path_folder,CONST.SAVE_CANDIDATES)
            if not os.path.isfile(path_candidates) or overwrite:
                self.candidates.clean_up_mols()
                store_candidates(path_candidates,self.candidates)
            else:
                logging.warning("File already exists: "+path_candidates+" already exist and won't be overwritten")
            path_features=os.path.join(path_folder,CONST.SAVE_FEATURES)
            if not os.path.isfile(path_features) or overwrite:
                store_features(path_features,self.features)
            else:
                logging.warning("File already exists: "+path_features+" already exist and won't be overwritten")
            path_GA =os.path.join(path_folder,CONST.SAVE_GA)
            if not os.path.isfile(path_GA) or overwrite:
                self.save_GA(path_GA)
            else:
                logging.warning("File already exists: "+path_GA+" already exist and won't be overwritten")

    def __len__(self):
        return self.GA.number_of_edges()

    def __str__(self):
        return "Annotation object with "+str(len(self.features))+" features and "+\
        str(len(self.candidates))+" candidates with "+\
        str(self.GA.number_of_edges())+" potential links."


def initial_cluster_annotation(rprobs,unknown_prob,draw_opt=False,uniform=False):
    unknown_idx = rprobs.shape[1]
    temp_unknown = np.repeat(unknown_prob,rprobs.shape[0]).reshape((-1,1))
    probs = np.concatenate([rprobs,temp_unknown],axis=1)
    NF = probs.shape[0]
    NC = probs.shape[1]
    ssidx = np.where(probs!=0)
    vprobs = probs[ssidx]
    if uniform:
        vprobs = np.ones(len(ssidx))
    NFV = (NF-1)
    all_edges = list(zip(ssidx[0],ssidx[1]))
    for idx in range(len(all_edges)):
        e1,e2 = all_edges[idx]
        if e2==unknown_idx:
            e2 = e1+NC+NF
        else:
            e2 = e2+NF
        all_edges[idx] = (e1,e2,{"v":vprobs[idx]})
    G = nx.Graph()
    G.add_edges_from(all_edges)
    vmatch = nx.max_weight_matching(G, weight='v')
    nvmatch = []
    new_annot = np.repeat(unknown_idx,NF)
    for vf,vc in vmatch:
        if vf>vc:
            vc,vf=vf,vc
        if vc>=(NF+NC):
            vc = unknown_idx
        else:
            vc = vc-NF
            nvmatch.append((vf,vc))
    if len(nvmatch)>0:
        i1,i2 = zip(*nvmatch)
        new_annot[np.array(sorted(i1))]=np.array(sorted(i2))

    ##We check the inital annotation, if there is a mistake we report it
    count_annot = Counter(new_annot.tolist())
    for key in count_annot:
        if count_annot[key]>2 and key!=unknown_idx:
            print("v1rprobs:",rprobs,"vmatch:",vmatch,"i1:",i1,"i2:",i2,"new_annot:",new_annot)
            raise Exception("Wrong clust")
        lval = -1
        for idx in range(NF):
            if new_annot[idx] != unknown_idx:
                if new_annot[idx]<=lval:
                    print("v2rprobs:",rprobs,"vmatch:",vmatch,"i1:",i1,"i2:",i2,"new_annot:",new_annot,"idx:",idx,"lval:",lval)
                    raise Exception("Wrong clust")
                else:
                    lval = new_annot[idx]
    return new_annot

def mixed_sample(annot,num_iteration=5000,initial_annotation=None,
path_samples = None, burn_in=100,isomers_burnin=5,
isomers_total=15,plotI=100,buffer_size = 50, vplot = False):
    """Short summary.

    Parameters
    ----------
    annot : type
        Description of parameter `annot`.
    num_iteration : type
        Description of parameter `num_iteration`.
    initial_annotation : type
        Description of parameter `initial_annotation`.
    path_samples : String
        Path to an hfd5 file to stroe the sample. It will we be overwritten or created.
    burn_in : type
        Description of parameter `burn_in`.
    isomers_burnin : type
        Description of parameter `isomers_burnin`.
    isomers_total : type
        Description of parameter `isomers_total`.
    plotI : type
        Description of parameter `plotI`.
    vplot : type
        Description of parameter `vplot`.

    Returns
    -------
    type
        THe samples and probablities

    """

    logging.info("Sarting annotation.")
    # We first extract the clusters
    fclusters = get_clusters(annot)

    #We initialize the sample storage
    storer = HDF5storer(path_samples,buffer_size = buffer_size)
    storer.initialize_fieds(annot.features,annot.links,annot.GA)

    if TIMER:
        timer_postpro = Timer()
        timer_links = Timer()
        timer_sampling = Timer()
        timer_prepro = Timer()
        timer_store = Timer()

    #All clusters are ordered retention time
    # cands_rts = [annot.rt_prop.compute_candidates(mol) for mol in annot.candidates]
    cands_rts = [annot.rt_property.compute_candidates(imols) for imols in chunks(list(range(len(annot.candidates))),5000)]
    cands_rts = list(itertools.chain(*cands_rts))
    feats_rts = annot.features.rt().to_numpy()

    #We reorder all the clusters by retention time
    fclusters = [(sorted(tclust[0], key=lambda x: feats_rts[x]),sorted(tclust[1],\
    key=lambda x: cands_rts[x-annot.num_features-1])) for tclust in fclusters]

    #Unknwonw idx
    p_unknown_prior = annot.GA.graph[CONST.UNKNOWN_PROB]

    # Cache for the prior of the clusters (Can be removed)
    prior_cache = {idx:prior_cluster(annot,clust) for idx,clust in enumerate(fclusters)}

    #We correctly initialize the cluster
    for clust_idx,clust_prob in prior_cache.items():
        clust_annot = initial_cluster_annotation(clust_prob,unknown_prob=p_unknown_prior)
        cfeats = fclusters[clust_idx][0]
        ccands = fclusters[clust_idx][1]
        for feat,cand in zip(cfeats,clust_annot):
            if cand==len(ccands):
                annot.GA.nodes[feat]["annotation"] = annot.unknown_label
            else:
                annot.GA.nodes[feat]["annotation"] = ccands[cand]

    #We need to reinitialize
    for link in annot.links:
        link.initialize(annot)
    #We take the first annotation
    current_annotation = np.array([annot.GA.nodes[feat]["annotation"] for feat in annot._features_iter()])

    #We compute the probability
    probs = []
    samples = [current_annotation]
    alphas = [0]

    #THis store the acceptance ratio for isomers MH
    alpha_isomers = 0
    count_isomers = 0

    #Store prior
    storer.store_prior(annot.GA)

    #Probability of an unknown annotation
    p_unknown_link = link_prob_unknown(annot)
    p_unknown = p_unknown_prior*p_unknown_link

    storer.set_unknown_prob(p_unknown_prior,p_unknown_link)
    storer.initalize_buffer_from_clusters(fclusters)

    #We reinitialize the data
    # print("STARTING ANNOTATION")
    for iter in tqdm.tqdm(range(num_iteration)):
        if MPL_FOUND and iter!=0 and iter//plotI==0 and vplot:
            plt.plot([1,2,4],[1,10,11])
            plt.ylabel("Log likehood")
            plt.xlabel("Iteration")
            plt.xlim(0,num_iteration)
            plt.show()

        #We generate a random permutation
        forder = np.random.permutation(len(fclusters))
        #We now compute it
        current_prob = 0
        initial_prob = 0
        for ifeat in forder:
            if TIMER:
                timer_prepro.tic()
            clust = fclusters[ifeat]
            cfeats = clust[0]
            ccands = np.array(clust[1]+[annot.unknown_label])
            # if len(cfeats)>1:
                # print("ifeat:",ifeat,"cfeats:",cfeats,"ccands:",ccands)
            #Unknown metabolite only
            if len(ccands)==1:
                continue

            #If there is no candidate it is an unknown
            prior_probs = prior_cache[ifeat]
            if TIMER:
                timer_links.tic()
            link_probs_nn = link_prob_cluster(annot,clust,current_annotation,annot.num_features)
            if TIMER:
                timer_links.toc()
            #We store the unnormalized probablity for each metrics of each features
            for idfeat,cifeat in enumerate(cfeats):
                storer.store_prob(cifeat,link_probs_nn[idfeat,:,:])
            link_probs = np.prod(link_probs_nn,axis=2)
            # Final probability
            full_probs = prior_probs*link_probs
            #We add the uknown probability
            temp_unknown = np.repeat(p_unknown,full_probs.shape[0]).reshape((-1,1))
            full_probs_nn = np.concatenate([full_probs,temp_unknown],axis=1)
            full_probs = full_probs_nn/(np.sum(full_probs_nn,axis=1)[:,None])
            #Saving the old annotation to do the update
            clust_old_annot = (current_annotation[cfeats]).copy()
            #One feature, just a sampling from candidates
            if TIMER:
                timer_prepro.toc()
            if len(cfeats)==1:
                if iter==0:
                    initial_prob += np.log(full_probs[0,np.where(ccands==(current_annotation[cfeats[0]]))])
                new_idx = np.random.choice(list(range(len(ccands))),p=full_probs[0,:])
                if TIMER:
                    timer_postpro.tic()
                if new_idx == len(ccands):
                    current_annotation[cfeats[0]] = annot.unknown_label
                else:
                    new_annot = ccands[new_idx]
                    current_annotation[cfeats[0]] = new_annot
                current_prob += np.log(full_probs[0,new_idx])
            else: #Many features
                z0 = current_annotation[cfeats]
                # TODO: Change that for a faster alternatives
                ic_index = {val:idx for idx,val in enumerate(ccands)}
                z0b = np.array([ic_index[x] for x in z0],dtype=np.intc)
                ##We store the matrix before running
                if TIMER:
                    timer_sampling.tic()
                ##THis is to frbug only
                #if 104 in cfeats:
                #    print("cfeats:\n{}ccands:\n{}z0:\n{}z0b:{}\nfull_probs:\n{}".format(cfeats,ccands,z0,z0b,full_probs))
                zn,current_alpha = isoclustcython.isomers_MH(full_probs,z0b,num_iterations = isomers_total, burn_in = isomers_burnin, last_only = True)
                if TIMER:
                    timer_postpro.tic()
                    timer_sampling.toc()
                alpha_isomers += current_alpha
                count_isomers += 1
                current_annotation[cfeats] = ccands[zn]
                pvals =  np.sum(np.log(full_probs[np.arange(len(cfeats)),zn]))
                if iter==0:
                    vold_annot = np.array([ic_index[x] for x in current_annotation[cfeats]])
                    initial_prob += np.sum(np.log(full_probs[np.arange(len(cfeats)),vold_annot]))
                if  np.isinf(pvals):
                    print("z0:",z0,"z0b:",z0b,"zn:",zn,"ic_index:",ic_index)
                    print("lfeats:",cfeats,"lcands:",ccands,"ifeat:",ifeat,"p:",full_probs.shape,"zn:",zn,
                    "fprobs:",full_probs[np.arange(len(cfeats)),z0b],
                    "full_probs:",full_probs)
                    #raise Exception("Oops")
                else:
                    current_prob += pvals
            clust_new_annot = current_annotation[cfeats]
            #Updating all the links objects
            update_annotation(annot,cfeats,clust_old_annot-annot.num_features-1,clust_new_annot-annot.num_features-1)
            if TIMER:
                timer_postpro.toc()

        timer_store.tic()
        #We pass to the next iteration
        storer.store_sample(current_annotation.copy())
        storer.next_iteration()

        #Store the sample
        probs.append(current_prob)
        if iter==0:
            probs.append(initial_prob)
        samples.append(current_annotation.copy())
        alphas.append(alpha_isomers/count_isomers)
        timer_store.toc()
    storer.finish_sampling()
    if TIMER:
        print("TIMER: PREPRO {:.2f} POST {:.2f} SAMP {:.2f} LINK {:.2f} STORE {:.2f}".format(timer_prepro.total(),timer_postpro.total(),timer_sampling.total(),timer_links.total(),timer_store.total()))

    return samples,probs,alphas

def get_clusters(annot):
    tannot = annot.GA.copy()
    tannot.remove_node(annot.unknown_label)
    clusters = [comp for comp in nx.connected_components(tannot)]
    vclusters = [None]*len(clusters)
    idx_cluster = 0
    for idx in range(len(clusters)):
        feats = [x for x in clusters[idx] if x<annot.num_features]
        cands = [x for x in clusters[idx] if x>= annot.num_features]
        if len(feats)==0:
            continue
        vclusters[idx_cluster] = (feats,cands)
        idx_cluster += 1

    return vclusters[0:idx_cluster]

def get_clusters_simple(GA,features,unknown):
    tannot = GA.copy()
    tannot.remove_node(unknown)
    clusters = [comp for comp in nx.connected_components(tannot)]
    vclusters = [None]*len(clusters)
    idx_cluster = 0
    for idx in range(len(clusters)):
        feats = [x for x in clusters[idx] if x<features.unknown_idx()]
        cands = [x for x in clusters[idx] if x>=features.unknown_idx()]
        if len(feats)==0:
            continue
        vclusters[idx_cluster] = (feats,cands)
        idx_cluster += 1

    return vclusters[0:idx_cluster]


def prior_cluster(annot,clust):
    feats,cands = clust
    #We compute the prior
    pmatrix = np.zeros((len(feats),len(cands)))
    #We compute the index
    cands_index = {key:idx for idx,key in enumerate(cands)}
    for idx_feat,ifeat in enumerate(feats):
        for icand in annot.GA[ifeat]:
            #If it is not in the cluster we ignore it
            if icand in cands_index and icand in annot.GA[ifeat]:
                pmatrix[idx_feat,cands_index[icand]] = annot.GA[ifeat][icand][CONST.PRIOR]
    return pmatrix

def link_prob_cluster(annot,clust,current_annotation,num_features):
    plinks = np.zeros(shape=(len(clust[0]),len(clust[1]),len(annot.links)),dtype=np.double)
    for ifeat,feat in enumerate(clust[0]):
        tcand = np.array(clust[1]) - num_features -1
        for ilink,link in enumerate(annot.links):
            #We check if the links is feature dependent
            probs = link.get_probs(feat,tcand,current_annotation)
            plinks[ifeat,:,ilink] = probs
    return plinks

def update_annotation(annot,feats_clust,old_annot,new_annot):
    for ifeat,feat in enumerate(feats_clust):
        if old_annot[ifeat] == new_annot[ifeat]:
            continue
        for ilink,link in enumerate(annot.links):
            #We could delegate that to each link
            link.update_annotation(feat,old_annot[ifeat],new_annot[ifeat])

def link_prob_unknown(annot):
    return np.prod(np.array([link.unknown_prob() for link in annot.links]))
