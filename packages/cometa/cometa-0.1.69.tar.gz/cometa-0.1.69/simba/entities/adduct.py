import re
import simba.constants as CONST
from rdkit.Chem import GetPeriodicTable
from simba.entities.molecule import MassCalculator
import numpy as np
import networkx as nx
import logging
from typing import List, Optional,Union


def make_default_adducts(polarity:Union[str,int]) -> List[str]:
    """[summary]

    Args:
        polarity (Union[str,int]): The polarity of the acquisition givne as a string or an integer.

    Returns:
        List[str]: A list of the adducts as strings.
    """
    polarity = CONST.parse_polarity(polarity)
    if polarity == CONST.POS:
        maina =  CONST.main_adducts_pos
        adducts = CONST.supp_adducts_pos
    else:
        maina = CONST.main_adducts_neg
        adducts = CONST.supp_adducts_neg
    return maina,adducts


def getAtomsSet():
    ptable = GetPeriodicTable()
    return set([ptable.GetElementSymbol(idx) for
    idx in range(1,CONST.rdkit_num_atoms)])

def make_symbol(atom,count):
    if count>1:
        return atom+str(count)
    return atom

class Formula:
    ref_atoms = getAtomsSet()
    regex = "[A-Z]{1}[a-z]?)([0-9]{0,3}"
    pattern = re.compile("("+regex+")")
    mass_calculator = MassCalculator()
    def __init__(self,string):
        matched = Formula.pattern.findall(string)
        atoms,counts = zip(*matched)
        #We control the atom
        if set(atoms).issubset(Formula.ref_atoms):
            self.atoms = atoms
            self.counts = [int(count) if count!="" else 1 for count in counts]
        else:
            incorrect = set(atoms).difference(Formula.ref_atoms)
            raise ValueError("Unknown atom(s): "+",".join(incorrect)+".")
    def get_mass(self):
        return Formula.mass_calculator.formula_mass(self.atoms,self.counts)
    def __str__(self):
        return "".join([make_symbol(atom,count) for atom,count in zip(self.atoms,self.counts)])

def str_polarity(intpol):
    if intpol == 1:
        return "+"
    return "-"


def make_adduct_symbol(formula,count,polarity) :
    polarity = str_polarity(polarity)
    if count>1:
        return polarity+str(count)+str(formula)
    return polarity+str(formula)

#An adduct is just a bunch of formula, with a charge at the end.
class Adduct:
    """Class used to handle a single adduct"""
    pat_adduct = re.compile("([\+\-])([0-9])?([a-zA-Z0-9]+)")
    pat_charge = re.compile("([0-9]?)([\+\-])$")
    pat_count = re.compile("^\[([0-9]?)M")

    def get_mass(self,mol):
        return (self.num*mol.monoisotopic_mass()+self.massdiff-self.polarity*CONST.MASS_ELECTRON)/self.charge

    def __init__(self,string:str,num:Optional[int]=None,is_main:bool=False):
        """Constructor of adduct

        The adduct should be given as a string 
        Args:
            string (str): String description of an adduct. Example : "[M+H]+","[M+Cl]-","[2M+H]+","[M+H+NH3]+"
            num (Optional[int], optional): [description]. In the general case should be left blank. Used internally.
            is_main (bool, optional): [description]. Is the adduct a main adduct, ie an adduct which can be present without other adducts.
        """        
        self.adducts = []
        self.factors = []
        self.counts = []
        self.main = is_main
        self.num = num
        cpos = 0
        m = Adduct.pat_adduct.search(string,pos=cpos)
        while m is not None:
            op,num,formula = (m.group(1),m.group(2),m.group(3))
            if op=="+":
                op = 1
            else:
                op = -1

            if num is None:
                num = 1
            else:
                num = int(num)
            # We parse the formula
            formula = Formula(formula)
            self.adducts.append(formula)
            self.factors.append(op)
            self.counts.append(num)

            # Next adducts
            cpos = m.span()[1]
            m = Adduct.pat_adduct.search(string,pos=cpos)

        # Charge detection
        mcharge = Adduct.pat_charge.search(string)
        num_charge = mcharge.group(1)
        if num_charge=="":
            num_charge = 1
        else:
            num_charge = int(num_charge)

        # Polarity
        polarity = mcharge.group(2)
        if polarity == "+":
            polarity = 1
        else:
            polarity = -1

        # Count of molecuels
        mcount = Adduct.pat_count.search(string)
        count = mcount.group(1)
        if count=="":
            count = 1
        else:
            count = int(count)
        self.charge = num_charge
        self.num = count
        self.polarity = polarity
        self.massdiff = self.compute_mass_diff()
        self.name = self.human_readable()
        #We create the serializaed version
        self.serialize()

    def compute_mass_diff(self):
        accu = 0
        for idx in range(len(self.adducts)):
            accu += self.adducts[idx].get_mass()*self.counts[idx]*self.factors[idx]
        return accu

    def is_precursor_adduct(self,item):
        if item.num>self.num:
            return False
        dic_formula = {str(form):count for form,count in zip(self.adducts,self.counts)}

        for f,c in zip(item.adducts,item.counts):
            sf = str(f)
            if sf in dic_formula:
                if dic_formula[sf]<c:
                    return False
            else:
                return False
        return True

    def is_direct_precursor_adduct(self,item):
        if item.num>self.num:
            return False
        dic_formula = {str(form):count for form,count in zip(self.adducts,self.counts)}
        total_diff = 0
        for f,c in zip(item.adducts,item.counts):
            sf = str(f)
            if sf in dic_formula:
                total_diff += (dic_formula[sf]-c)
                dic_formula[sf]=0
            else:
                return False
            if total_diff>1:
                return False
        #We add any missing elements
        total_diff += sum(dic_formula.values())
        #We add the supplementary molecule
        total_diff += (self.num-item.num)
        if total_diff==1:
            return True
        return False

    def serialize(self):
        formula_str = sorted([make_adduct_symbol(adduct,count,factor) for adduct,factor,count
         in zip(self.adducts,self.factors,self.counts)])
        formula_str ="_".join(formula_str)
        self_str = ["C"+str(self.charge)]+["N"+str(self.num)]+[formula_str]
        self_str = "|".join(self_str)
        self.id = self_str

    def __eq__(self,other):
        return self.id==other.id

    def human_readable(self):
        str_num = ""
        if self.num>1:
            str_num = str(self.num)
        str_charge = ""
        if self.charge>1:
            str_charge = str(self.charge)
        prefix = "["+str_num+"M"
        suffix = "]"+str(str_charge)+str_polarity(self.polarity)
        formula_str = [make_adduct_symbol(adduct,count,factor) for adduct,factor,count
         in zip(self.adducts,self.factors,self.counts)]
        formula_str = "".join(formula_str)
        return prefix+formula_str+suffix

    def __str__(self):
        return self.name

    def is_main(self):
        return self.main

    def set_num(self,num):
        self.num = num

    def get_num(self):
        return self.num



def build_adducts_adjacency_matrix(adducts):
    adjs = np.zeros(shape=(len(adducts),len(adducts)))
    for i in range(len(adducts)):
        for j in range(len(adducts)):
            if i==j: continue
            if adducts[i].is_precursor_adduct(adducts[j]):
                 adjs[j,i] = adducts[i].is_direct_precursor_adduct(adducts[j])
    return adjs



class AdductsTree:
    def __init__(self,adducts:List[str],main_adducts:List[str]):
        """Create an adduct hierarchy

        Args:
            adducts (List[str]): A list of all the adducts given a string. It should include "main_adducts"
            main_adducts (List[str]): A list of the main adducts, the adducts which can be detecte by themselves

        Raises:
            ValueError: A main adduct is not detected in the list.
        """        
        logging.info("Parsing adducts.")
        sadducts = set(adducts)
        smain = set(main_adducts)

        if len(smain.difference(sadducts))>0:
            raise ValueError("All the main adducts should be included into the adducts list, missing:"+str(smain.difference(sadducts)))
        self.adducts = [Adduct(add,num=idx) for idx,add in enumerate(adducts)]

        #We tage the correct adducts as main
        for idx_add in range(len(adducts)):
            if adducts[idx_add] in smain:
                self.adducts[idx_add].main = True
        self.adducts_name = [str(add) for add in self.adducts]
        self.main_adducts = [Adduct(add,is_main=True) for add in main_adducts]
        self.main_adducts_name = [str(add) for add in self.main_adducts]
        self.indices=set(list(range(0,len(self.adducts))))
        #We alway find the main adducts in adducts
        try:
            self.main_index = [self.adducts_name.index(m)\
             for m in self.main_adducts_name]
        except ValueError:
            missed = (set(self.main_adducts_name).difference(self.adducts_name))
            raise ValueError("Missing main adducts in the adducts list: "+str(list(missed)))

        logging.info("Building adducts trees.")
        adjs = build_adducts_adjacency_matrix(self.adducts)
        self.graph = nx.convert_matrix.from_numpy_matrix(adjs,create_using=nx.DiGraph)
        for idx,name in enumerate(self.adducts_name):
            self.graph.nodes[idx]["name"]=name
        self.trees={}
        self.unused_nodes=[]
        self.find_trees()

        # We set the index of the adducts

    def find_trees(self):
        self.indices = set([])
        for mainidx in range(len(self.main_adducts)):
            main = self.main_adducts[mainidx]
            try:
                index = self.adducts.index(main)
            except ValueError:
                continue
            descs = nx.descendants(self.graph,index)
            descs.add(index)
            for d in descs:
                self.indices.add(d)
            subtree = nx.subgraph(self.graph,descs)
            #We add the different dataset
            self.trees[self.main_adducts_name[mainidx]] = subtree
        full_indices = set(self.graph.nodes())
        self.unused_nodes = list(full_indices.difference(self.indices))
        cadducts = [self.adducts_name[idx] for idx in self.indices]
        self.main_index = [cadducts.index(m)\
         for m in self.main_adducts_name]
        #We relabel the trees
        new_mapping = {val:idx for idx,val in enumerate(self.indices)}
        for k in self.trees:
            self.trees[k] = nx.relabel_nodes(self.trees[k],new_mapping)

    def generate_edges(self):
        set_edges = set([])
        for tree in self.trees.values():
            for edge in tree.edges():
                set_edges.add(edge)
        return list(set_edges)


    def mass_modifications(self):
        nums = [add.num for add in self.adducts]
        massdiffs = [add.massdiff for add in self.adducts]
        charge =  [add.charge for add in self.adducts]
        return np.array(massdiffs),np.array(nums),np.array(charge)

    def __len__(self):
        return len(self.indices)

    def __iter__(self):
        for idx in self.indices:
            yield self.adducts[idx]

    def __str__(self):
        main_str = ",".join(self.main_adducts_name)
        summary_str = " ".join(["A set of adducts containing",str(len(self.adducts)),
        "adducts with main adducts",main_str+"."])
        if len(self.unused_nodes)==0:
            supp_str = "All adducts are reachable."
        else:
            supp_str = str(len(self.unused_nodes))+\
            " adducts are not reachable: "+",".join([self.adducts_name[ix] for ix in self.unused_nodes])
        return summary_str+supp_str



if __name__=="__main__":

    """This is some example code."""
    add_list = ["[2M+H+Na]2+","[M+Na-NH3]+","[M+Na]+","[M+H]+","[2M+H]+","[M+2H]2+"]
    adds = [Adduct(add) for add in add_list]
    adds = sorted(adds,key=lambda x:x.massdiff)
    add_str = [str(add) for add in adds]
    [str(aa) for aa in adds]
    f = Formula("C10H5Na1")
    f.get_mass()
    str(f)

    ex_adduct = "[2M+H+Na]+"
    ex_sub_adduct = "[M+Na-NH3]+"
    add = Adduct(ex_adduct)
    subadd = Adduct(ex_sub_adduct)
    add.is_precursor_adduct(subadd)


    add1 = "[M+H+Na]2+"
    add2 = "[M+Na+H]2+"
    a1 =Adduct(add1)
    a2 = Adduct(add2)
    a1.id
    a2.id
    a1==a2

    from simba.entities.molecule import sibMol

    smol = sibMol("CCCCCCCCC")
    smol.monoisotopic_mass()
    add.get_mass(smol)


    #Test of the adjacency matrix
    main_list = ["[M+Na]+","[M+H]+"]
    add_list = ["[2M+H+Na]2+","[M+Na-NH3]+","[M+Na]+","[M+H]+","[2M+H]+","[M+2H]2+","[2M+2U]3+"]
    atrees = AdductsTree(add_list,main_list)
    vv = atrees.mass_modifications()
    vv
    def neutral_mass(mz,mdiff,num,charge):
        return (mz*charge-mdiff)/num
    mm = 275.2

    neutral_mass(mm,vv[0],vv[1],vv[2])

    print(atrees)
    len(atrees)
    for add in atrees:
        print(add)
    str(atrees)
    atrees.indices
