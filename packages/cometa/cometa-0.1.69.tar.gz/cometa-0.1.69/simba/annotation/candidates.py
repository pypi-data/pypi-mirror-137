from simba.entities.molecule import sibMol,sibMolAdduct
from simba.entities.adduct import AdductsTree,make_default_adducts
import simba.constants as CONST
import numpy as np
import logging
import pandas as pd
import networkx as nx

#THis function remove computed descriptros and make the molecule pickable.
def _clean_mol(mol,all_keys=None):
    if all_keys is None:
        all_keys = list(vars(mol).keys())
    for k in all_keys:
        delattr(mol,k)

def _clean_list(vlist,to_remove):
    to_remove.sort()
    for idr in to_remove[::-1]:
        del vlist[idr]


class Candidates:
    def __init__(self,mols,supp_df=None,**kwargs):
        """A set of candidates metabolites.

        Parameters
        ----------
        mols : List of rdmol objects
            A list of rmols object as created by buildSibMolsFromList().
        supp_df : DataFrame
            A DataFrame containing the supplementary informations in the data.
        **kwargs : Iterable
            Supplementary informations to be stored, must be of the same size the mols.

        Returns
        -------
        Candidates
            A candidates objects.
        """
        self.mols = mols
        self.supp_infos = {}
        for key, value in kwargs.items():
            if len(value)!=len(self.mols):
                raise ValueError("Too many values in '"+key+"'")
            self.supp_infos[key] = value
        if supp_df is not None:
            for col in supp_df.columns:
                self.supp_infos[col] = supp_df[col].to_list()

        ##We remove all the duplicated elements now.


        self.masses = np.array([sibMol.monoisotopic_mass(x) for x in self.mols])
        self.idx = np.argsort(self.masses)


    def _get_sorted_masses(self):
        return self.masses[self.idx]

    def merge_duplicated_ids(self):
        to_remove = np.where(pd.Series([mol.get_id() for mol in self]).duplicated())
        logging.warning("Found "+str(len(to_remove))+" duplicated ids")
        _clean_list(self.mols,to_remove)
        for col in self.supp_infos:
            _clean_list(self.supp_infos[col],to_remove)

    def find_masses_windows(self,window):
        vmasses = self._get_sorted_masses()
        lb,ub = window
        lb = np.searchsorted(vmasses,lb)
        ub = np.searchsorted(vmasses,ub)
        to_return = self.idx[range(lb,ub)]
        return to_return

    def find_masses(self,mass,ppm=10,dmz=0.005):
        tol = ppm*mass*1e-6
        if tol<dmz:
            tol = dmz
        to_return = self.find_masses_windows((mass-tol,mass+tol))
        return to_return

    def list_infos(self):
        return list(self.supp_infos.keys())

    def get_info(self,info,idx):
        return self.supp_infos[info][idx]

    def reduce_candidates(self,cset):
        cidx = sorted(list(cset))
        logging.info("Reduced candidates set from "+str(len(self.mols))+" to "+str(len(cidx))+".")
        self.mols = [self.mols[idx] for idx in cidx]
        self.masses = self.masses[np.array(cidx)]
        self.idx = np.argsort(self.masses)
        for name in self.supp_infos:
            self.supp_infos[name] = [self.supp_infos[name][idx] for idx in cidx]

    def inchi_mols(self):
        temp = [m.get_inchi() for m in self]


    def clean_up_mols(self):
        #We check if the molecules need cleaning
        vars_dict = list(vars(self.mols[0].mol).keys())
        if len(vars_dict) == 0:
            logging.info("candidates clean-up function called but no clean-up is needed.")
        else:
            self._clean_up_mols(vars_dict)

    def _clean_up_mols(self,vdict):
        for mol in self.mols:
            _clean_mol(mol.mol)


    def __iter__(self):
        for mol in self.mols:
            yield mol

    def __len__(self):
        return len(self.mols)

    def __getitem__(self,index):
        return self.mols[index]

    def __str__(self):
        return "Candidates set containing "+str(len(self.mols))+" molecules with informations "+\
        ",".join(self.list_infos())+"."




class CandidatesA(Candidates):
    def __init__(self,mols,tadducts=None,supp_df=None,polarity="positive",**kwargs):
        self.polarity = CONST.parse_polarity(polarity)
        logging.info("Polarity detected: "+self.polarity)
        if tadducts is None:
            logging.info("Default adducts list used.")
            main_adducts,supp_adducts = make_default_adducts(self.polarity)
            tadducts = AdductsTree(supp_adducts,main_adducts)
        if not isinstance(tadducts,AdductsTree):
            raise TypeError("tadducts should be an 'AdductsTree' object.")
        #We first generate the metabolites.
        super(CandidatesA,self).__init__(mols,supp_df=supp_df,**kwargs)

        #We generate all the adducts idx
        na = len(tadducts)
        nc = len(self.mols)
        self.adduct_idx = np.repeat(np.arange(0,nc),na)
        self.adducts = tadducts

        #TODO parallelize
        # Define the ocmbined metabolies
        self.amols = [sibMolAdduct(mol,add) for mol in self.mols for\
         add in tadducts]

        #We then reorder given the masses
        self.masses = np.array([x.monoisotopic_mass() for x in self.amols])
        self.idx = np.argsort(self.masses)

        #BUilding the complete graph with every edges
        edges = self.adducts.generate_edges()
        nadducts = len(self.adducts)
        redges = np.tile(np.array(edges).T,nc)
        rmols = np.repeat(np.array(np.arange(nc))*nadducts,len(edges))
        all_edges = (rmols+redges)
        all_edges = all_edges.T
        self.graph = nx.DiGraph()
        self.graph.add_edges_from(all_edges)

    def list_infos(self):
        return list(self.supp_infos.keys())+["adduct"]

    #We update the supplementary infos with an adduct fields
    def get_info(self,info,idx):
        if info=="adduct":
            return str(self.amols[idx].adduct)
        return self.supp_infos[info][self.adduct_idx[idx]]

    #TODO add the tree graph removal.
    def reduce_candidates(self,cset):
        cidx = sorted(list(cset))
        #We remove nodes unrachable form a precursor
        #We first extract the main idx
        main_cidx = [cc for cc in cidx if (cc%len(self.adducts) in self.adducts.main_index)]
        #We build the subgraph
        sgraph = nx.subgraph(self.graph,cidx)
        new_cidx = set([])
        #We recreate the set of point
        sel_main = np.array(main_cidx)//len(self.adducts)
        cidx = np.repeat(sel_main*len(self.adducts),len(self.adducts))+np.tile(np.arange(len(self.adducts)),len(sel_main))
        cidx = sorted(list(set(cidx.tolist())))
        self.graph = nx.subgraph(self.graph,cidx)
        #We relabel the nodes
        nlabel = {val:idx for idx,val in enumerate(cidx)}
        self.graph = nx.relabel_nodes(self.graph,nlabel)
        logging.info("Reduced candidates set from "+str(len(self.amols))+" to "+str(len(cidx))+".")
        self.amols = [self.amols[idx] for idx in cidx]
        # Relabels the adduct_idx ot the correct ones
        self.adduct_idx = self.adduct_idx[np.array(cidx)]
        #We relabel the adduct idx to avoid gaps
        #!!!We need to close the gaps
        unique_mols_idx = np.unique(self.adduct_idx)
        trans = {val:idx for idx,val in enumerate(unique_mols_idx)}
        self.adduct_idx = np.array([trans[idxx] for idxx in self.adduct_idx])

        ###We also reduce the mols sets.
        self.mols = [self.mols[xx] for xx in unique_mols_idx]
        for key in self.supp_infos:
            self.supp_infos[key] = [self.supp_infos[key][xx] for xx in unique_mols_idx]
        self.masses = self.masses[np.array(cidx)]
        self.idx = np.argsort(self.masses)
        return trans

    def get_clusters_idx(self, key):
        #We just expand the selection until we are in a different cluster
        lbound = key
        rbound = key
        while lbound>0 and self.adduct_idx[lbound-1]==self.adduct_idx[key]:
            lbound -= 1
        while rbound<(len(self.adduct_idx)-1) and self.adduct_idx[rbound+1]==self.adduct_idx[key]:
            rbound += 1
        return list(range(lbound,rbound+1))

    def adduct_mols(self):
        return [m.get_adduct_str() for m in self]

    def __getitem__(self, key):
        if isinstance(key,slice):
            return self.amols[key]
        if isinstance(key,np.int64):
            key = int(key)
        if isinstance(key,float):
            key = int(key)
        if isinstance(key,int):
            return self.amols[int(key)]
        else:
            return self.amols[int(key[1:])]

    def __iter__(self):
        for mol in self.amols:
            yield mol

    def __len__(self):
        return len(self.amols)

    def __str__(self):
        return "Candidates set "+self.polarity+" containing "+str(len(self.amols))+" molecules with adducts "+\
        str([str(add) for add in self.adducts])+" with informations "+str(self.list_infos())+"."


if __name__=="__main__":
    pass
