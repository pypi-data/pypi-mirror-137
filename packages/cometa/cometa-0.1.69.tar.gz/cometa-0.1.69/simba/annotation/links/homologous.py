import networkx as nx
import numpy as np
import logging

import simba.annotation.links.homologous_functions as sah
from simba.annotation import scoring
from simba.annotation.generic.abstract_link import AnnotationLink


##THis is the geneirc class which should be generic
class HomologousLinks(AnnotationLink):

    def __init__(self,scorer=None,**kwargs):
        ##Cache of rthe subformula relationship
        self.cache_pair = {}
        if scorer is None:
            logging.info("No scorer provided, sigmoid scorer used.")
            self.scorer = scoring.build_sigmoid()
        else:
            self.scorer = scorer
        



    def cluster(self,features,**kwargs):
        # If parameters are missing we detemrine it
        if "rttol" not in kwargs:
            rtmax = features.rt().max()
            rttol = rtmax*0.015

        if "minlen" not in kwargs:
            minlen = 6

        clusters = sah.compute_homologuous_cluster(features,rttol=float(rttol),minlen=float(minlen),**kwargs)
        #We reorder by mass for simplicity
        clusters = [sorted(clust,key=lambda x: features.mz().iloc[x]) for clust in clusters]
        return clusters

    # To implement
    def is_linked_candidates(self,icand1,icand2):
        if (icand1,icand2) in self.cache_pair:
            return self.cache_pair[(icand1,icand2)]
        else:
            cand1 = self.candidates[icand1]
            cand2 = self.candidates[icand2]
            val = sah.is_subformula(cand2,cand1)
            self.cache_pair[(icand1,icand2)] = val
            self.cache_pair[(icand2,icand1)] = val
            return val

    def initialize(self,annotation,**kwargs):
        self.features = annotation.features
        self.candidates = annotation.candidates
        self.num_features = len(self.features)
        clusters = self.cluster(self.features,**kwargs)
        self.initialize_clusters(clusters)

    def initialize_clusters(self,clusters):
        self.clusters = clusters
        self.index = {}
        # Initialize each cluster
        for idx,clust in enumerate(clusters):
            # We index the data
            for feat in clust:
                if feat in self.index:
                    self.index[feat].add(idx)
                else:
                    self.index[feat] = set([idx])
        #We convert all the index to list
        for key in self.index.keys():
            self.index[key]=list(self.index[key])

    def related_features(self,feat):
        if feat not in self.index:
            return []
        else:
            return [self.clusters[idx] for idx in self.index[feat]]

            #Count neighbours for a signle candidates
    def count_neighbours_candidate(self,feat,cand,current_annotation):
        #Shortcut not in cluster
        if feat not in self.index: return 0
        clust_feat = self.related_features(feat)
        linked = 0
        for fidx in clust_feat:
            if fidx==feat:
                continue
            ncand = current_annotation[fidx]-self.num_features
            linked +=  self.is_linked_candidates(cand,ncand)

        return linked


    def count_neighbours_candidates(self,feat,cands,current_annotation):
        #Shortcut not in cluster
        if feat not in self.index: return np.zeros((len(cands),))+0.1
        clusters_feat = self.related_features(feat)
        linkeds = []
        for cand in cands:
            linked = 0
            for cluster_feat in clusters_feat:
                for fidx in cluster_feat:
                    if fidx==feat:
                        continue
                    ncand = current_annotation[fidx]-self.num_features
                    linked +=  self.is_linked_candidates(cand-self.num_features,ncand)
            linkeds.append(linked)
        return np.array(linkeds)

    #Let s hope that we can improve this, this is so inefficient
    def update_annotation(self,feat,old_annot,new_annot):
        pass

    def unknown_prob(self):
        return self.scorer(0)

    # def get_prob(self,feat,candidate,current_annotation):
    def get_probs(self,feat,candidates,current_annotation):
        linked_vals = np.array(self.count_neighbours_candidates(feat,candidates,current_annotation),dtype=np.uint8)
        # print(linked_vals)
        return self.scorer(linked_vals)

    

    def __str__(self):
        return "Features clusters containing "+str(len(self.clusters))+" clusters."
