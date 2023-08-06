import numpy as np
from scipy.sparse import csr_matrix
import networkx as nx
import logging
from simba.annotation.generic.abstract_link import AnnotationLink
from simba.annotation.scoring import exp_diff
from simba.utils.arguments_checking import check_range,check_type


##operation to do, given an adduct and a molecule check iuf all its parent molecules exists. If so get the current annotations
##We sotre the struvture in a dictionnary molid(int)_adductid(int): feat_id(int)

def make_adduct_key(mol):
    return "{0}_{1}".format(mol.get_id(),mol.adduct.num)

def make_node_key(feat_clust,cand):
    str(feat_clust)+"_"+make_adduct_key(cand)


class AdductsLinks(AnnotationLink):
    def __init__(self,drt:float=0.1,ppm:float=10,dmz:float=0.007,main_prob:float = 1.0, 
    min_prob:float=0.001,cor_threshold:float=0.5,full_parents:bool=False):
        """Initialize an adduct Link object

        Args:
            drt (float, optional): Tolerance in retention time. Defaults to 0.1.
            ppm (float, optional): Tolerance in ppm. Defaults to 10.
            dmz (float, optional): Tolerance in mass. Defaults to 0.007.
            main_prob (float, optional): Probability of a main adduct. Defaults to 1.0.
            min_prob (float, optional): Probability of an adduct without parent. Defaults to 0.001.
            cor_threshold (float, optional): A correlation threshold above which the adduct won't be annotated. Defaults to 0.5.
            full_parents (bool, optional): Shall all the parents adduct be detected or only one. Defaults to False.
        """
        self.drt = check_range(drt,(0.005,1.5))
        self.ppm = check_range(ppm,(0.5,100))
        self.dmz = check_range(dmz,(0.0005,0.5))
        self.main_prob = check_type(main_prob,float)
        self.min_prob = check_type(min_prob,float)
        self.full_parents = check_type(full_parents,bool)
        self.cor_threshold = check_range(cor_threshold,(0,1.0))


    def initialize(self,annotation,**kwargs):
        """Initialize the 

        Args:
            annotation (SimAnnotator): A SimAnnotator object used to check annotated candidates.
        """
        self.annotation = annotation
        self.features = annotation.features
        self.candidates = annotation.candidates
        self.rts = self.features.rt()
        self.rt_idx = np.argsort(self.rts).to_numpy()
        #We store the current rt corresponding to each candidates
        self.mol_rt = {}
        self.mol_count = {}
        #Initializing the graph
        self.graph = nx.Graph()
        nodes_to_add = list(range(len(self.features)))
        self.graph.add_nodes_from(nodes_to_add)
        self.generate_features_links(drt=self.drt,ppm=self.ppm,dmz=self.dmz)
        self.current_adducts = {}
        #We compute the predecessors of each adduct
        #Just for lisibility
        g_adduct = self.candidates.adducts.graph
        self.parents_adducts = {nn:list(g_adduct.predecessors(nn)) for nn in g_adduct.nodes()}
        self.unknown_label = self.annotation.unknown_label
        self.compute_correlation()

        #This dictionnary stores the fact that at least one main adduct is in the correct mass range
        self.out_bounds = set([])
        mz_range = self.features.mz_range()
        for cand in self.candidates:
            if cand.mass>mz_range[1] or cand.mass<mz_range[0]:
                self.out_bounds.add(cand.get_id())

        num_features = len(annotation.features)
        for ifeat in range(num_features):
            ifeat_annot = annotation.GA.nodes[ifeat]["annotation"]-num_features-1
            clust_feat = self.graph.nodes[ifeat]["c"]
            cand_annot = annotation.candidates[ifeat_annot]
            cid = cand_annot.get_id()
            self.mol_rt[cid] =  self.rts[ifeat]
            if cid not in self.mol_count:
                self.mol_count[cid] = 1
            else:
                self.mol_count[cid] += 1
            vkey = make_node_key(clust_feat,cand_annot)
            self.current_adducts[vkey] = ifeat
        # self.correlation_matrix = csr_matrix(shape=(num_features,num_features),dtype=np.float)


    def generate_features_links(self,drt=0.1,ppm=10,dmz=0.007):
        mzs = self.features.mz().to_numpy()
        self.drt = drt/2
        sorted_rts = self.rts.iloc[self.rt_idx].to_numpy()
        massdiffs,nums,charges = self.candidates.adducts.mass_modifications()

        #We compute the nuetral mass
        def cneutral_mass(mz,mdiff,num,charge):
            return (mz*charge-mdiff)/num

        initial_lb = 0
        initial_ub = 0
        lb = 0
        ub = 0
        count_edges = 0
        #We extract all the possible adducts
        for iidx,idx in enumerate(self.rt_idx):
            ##Filter in retention time
            ub = initial_ub
            lb = initial_lb
            crt = sorted_rts[iidx]
            while lb<len(self.rt_idx) and sorted_rts[lb]<(crt-drt):
                lb += 1

            while ub<len(self.rt_idx) and sorted_rts[ub]<(crt+drt):
                ub += 1

            if (lb+1) == ub:
                continue
            mz = float(mzs[self.rt_idx[iidx]])
            idx_coelute = self.rt_idx[lb:ub]
            initial_lb = lb
            initial_ub = ub
            #To avoid double counting, we remove the lower masses
            sel_val  = mzs[idx_coelute]>mz
            idx_coelute = idx_coelute[sel_val]
            if len(idx_coelute)==0: continue
            mz_coelute = mzs[idx_coelute]
            #We test every adduct hypothesis
            neutral_mass = cneutral_mass(mz,massdiffs,nums,charges)
            coelute_mass = [cneutral_mass(mza,massdiffs,nums,charges) for mza in mz_coelute]

            #We build the coleute mass in a matrix
            coelute_mass = np.vstack(coelute_mass)
            tol = ppm*mz*1e-6
            if tol<dmz:
                tol = dmz
            #Every case is an aduct hypothesis for the data
            # TODO: Put that into separate threads
            for nidx in range(len(neutral_mass)):
                selected = np.abs(neutral_mass[nidx] - coelute_mass)<tol
                sel_row,sel_col = np.where(selected)
                #We remove when it is the same adduct

                if len(sel_row)==0: continue
                edges_to_add = [(self.rt_idx[iidx],idx_coelute[irow],{"v":(nidx,icol)}) for irow,icol in zip(sel_row,sel_col)]
                self.graph.add_edges_from(edges_to_add)
                count_edges += len(edges_to_add)
        #We also stroe the component infomrations
        for icomp,comp in enumerate(nx.connected_components(self.graph)):
            for node in comp:
                self.graph.nodes[node]["c"] = icomp
        logging.info("Potential adduct links found: "+str(count_edges)+".")

    def compute_correlation(self):
        int_matrix = self.features.intensities().to_numpy()
        logging.info("Computing correlations to confirm adducts")
        c1,c2 = zip(*[(a,b) for a,b in self.graph.edges()])
        correlations = np.array([np.corrcoef(int_matrix[a,:],int_matrix[b,:])[0,1] for a,b in self.graph.edges()])
        self.correlation_matrix = csr_matrix((correlations,(c1,c2)),shape=(len(self.features),len(self.features)))
        #Given an annotation we check if there is acoherent addcuts in the data
    
    def get_rt_mol_factor(self,feat,cand):
        cid = cand.get_id()
        feat_rt = self.rts[feat]
        if cid in self.mol_rt:
            return 0.1+2*exp_diff(self.mol_rt[cid]-feat_rt,self.drt)
        else:
            #Value at 0
            return 1.0

    def get_prob(self,feat,candidate,current_annotation):
        mcand = self.candidates[candidate]
        rt_factor = self.get_rt_mol_factor(feat,mcand)
        if mcand.adduct.is_main():
            return self.main_prob*rt_factor

        if mcand.get_id() in self.out_bounds:
            return self.main_prob*0.5
        # We get the number of feature
        linked_features = self.graph[feat]
        if len(linked_features)==0:
            return self.min_prob

        #We get the feature clusters
        feat_clust = self.graph.nodes[feat]["c"]
        parent_set = set(self.parents_adducts[mcand.adduct.num])

        accu_prob = 0.0
        vcount = 0
        for pnum in parent_set:
            key_parent = "_".join([str(feat_clust),str(mcand.get_id()),str(pnum)])
            if key_parent in self.current_adducts:
                parent_feat = self.current_adducts[key_parent]
                accu_prob += max(self.correlation_matrix[feat,parent_feat],self.correlation_matrix[parent_feat,feat])
                vcount += 1
            elif self.full_parents:
                return self.min_prob
        if vcount == 0:
            return self.min_prob
        accu_prob = accu_prob/vcount
        if accu_prob<self.cor_threshold:
            return self.min_prob
        else:
            return self.main_prob*(0.5+rt_factor)+exp_diff(accu_prob,0.5)

    def get_probs(self,feat,cands,current_annotation):
        probs = np.array([self.get_prob(feat,cand,current_annotation) for cand in cands])
        return probs

    # TODO: Conveninent function. Update if this can be made efficient one way or another.
    def update_annotation(self,feat,old_annot,new_annot):
        feat_clust = self.graph.nodes[feat]["c"]
        old_mol = self.candidates[old_annot]
        new_mol = self.candidates[new_annot]
        old_key = make_node_key(feat_clust,old_mol)
        new_key = make_node_key(feat_clust,new_mol)
        old_id = old_mol.get_id()
        new_id = new_mol.get_id()

        if old_key != new_key:
            del self.current_adducts[old_key]
            self.current_adducts[new_key] = feat
            new_rt = self.rts[feat]
                #We update the mean RTs
            if new_id in self.mol_rt:
                # The new one
                self.mol_rt[new_id] = (self.mol_rt[new_id]*self.mol_count[new_id]+new_rt)/(self.mol_count[new_id]+1)
                self.mol_count[new_id] += 1
            else:
                self.mol_rt[new_id] = new_rt
                self.mol_count[new_id] = 1
                # The old one
            if self.mol_count[old_id]==1:
                del self.mol_count[old_id]
                del self.mol_rt[old_id]
            else:
                self.mol_rt[old_id] = (self.mol_rt[old_id]*self.mol_count[old_id]-new_rt)/(self.mol_count[old_id]-1)
                self.mol_count[old_id] -= 1

    def unknown_prob(self):
        return self.main_prob
