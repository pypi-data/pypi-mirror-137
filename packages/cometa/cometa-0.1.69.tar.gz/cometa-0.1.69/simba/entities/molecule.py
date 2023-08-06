import importlib
import logging

from rdkit import RDLogger
import rdkit.Chem

from rdkit.Chem.rdchem import Mol
from rdkit.Chem import MolFromSmiles,CanonSmiles,GetPeriodicTable, AddHs
from rdkit.Chem.Descriptors import ExactMolWt
from rdkit.Chem.rdmolfiles import SDMolSupplier
import multiprocessing as mp

from pandas import Series

##THis is python version dependent to correctly import the inchi
SMB_HAS_INCHI = False
if hasattr(rdkit.Chem,"MolFromInchi"):
    from rdkit.Chem import MolFromInchi,MolToInchiKey,MolToInchi
    SMB_HAS_INCHI = True
else:
    from rdkit.Chem.inchi import INCHI_AVAILABLE
    logging.warning("InChI rdkit module not available.")
    SMB_HAS_INCHI = False
    if INCHI_AVAILABLE:
        SMB_HAS_INCHI = True
        from rdkit.Chem.inchi import MolFromInchi,MolToInchiKey,MolToInchi


# A monoisotopic mass calculator
class MassCalculator:
    def __init__(self):
        self.ptable = GetPeriodicTable()

    def monoisotopic_mass(self,mol):
        mol = AddHs(mol)
        mass = sum([self.ptable.GetMostCommonIsotopeMass(atom.GetSymbol()) for atom in mol.GetAtoms()])
        return mass

    def atom_mass(self,atom):
        return self.ptable.GetMostCommonIsotopeMass(atom)

    def formula_mass(self,atoms,counts):
        return sum([count*self.ptable.GetMostCommonIsotopeMass(atom) for atom,count in zip(atoms,counts)])

###Parsing function
class sibMol:
    
    key_function = lambda x:x
    initialised = False
    mass_calculator = MassCalculator()

    ###Stati method used onlly to make the keys fast.
    @staticmethod
    def make_key_function():
        if SMB_HAS_INCHI:
            logging.info("InchiKey used as id")
            def planar_inchikey(mol):
                return MolToInchiKey(mol)[0:14]
            sibMol.key_function = planar_inchikey
        else:
            logging.info("Inchi installation not found in rdkit, using Canonical smiles as id.")
            sibMol.key_function = CanonSmiles

    ###Static method used only to compute the id.
    @staticmethod
    def compute_id(smol):
        if not sibMol.initialised:
            sibMol.make_key_function()
        return sibMol.key_function(smol)

    @staticmethod
    def compute_monoisotopic_mass(smol):
        return sibMol.mass_calculator.monoisotopic_mass(smol.mol)

    @staticmethod
    def compute_inchi(smol):
        return MolToInchi(smol.mol)

    def __init__(self,mol):
        ###SMILES or INCHI
        if isinstance(mol,sibMol):
            self.mol = mol.mol
            self.id = mol.id
            self.mass = mol.mass
            self.structure = None
        else:
            if isinstance(mol,str):
                try:
                    if mol.startswith("InChI") :
                        if SMB_HAS_INCHI:
                            mol = MolFromInchi(mol)
                        else:
                            raise TypeError("Impossible to read InChi when the rdkit was not compiled with it.")
                    else:
                        mol = MolFromSmiles(mol)
                    self.structure = mol
                except Exception as e:
                    raise ValueError("Impossible to convert input",mol,"to a valid molecular structure")
            ##SDF
            self.mol = mol
            self.id = sibMol.compute_id(self.mol)
            self.mass = sibMol.compute_monoisotopic_mass(self)

    def rdmol(self):
        return self.mol

    def to_inchi(self):
        return MolToInchi(self)

    ###id can be changed to anything
    def get_id(self):
        return self.id

    def monoisotopic_mass(self):
        return self.mass

    def compute_inchi(self):
        self.structure = sibMol.compute_inchi(self)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self,other):
        return hash(self)==hash(other)

    def __str__(self):
        return str(self.get_id())

class sibMolAdduct(sibMol):
    @staticmethod
    def compute_monoisotopic_mass(amol):
        return amol.adduct.get_mass(amol) 

    def __init__(self,mol,adduct):
        self.adduct = adduct
        super(sibMolAdduct, self).__init__(mol)
        self.mass = sibMolAdduct.compute_monoisotopic_mass(self)

    def in_mzrange(self,mzrange):
        return mzrange[0]<self.mass and mzrange[1]>self.mass

    def get_adduct_str(self):
        return str(self.adduct)

    def get_id(self):
        return super(sibMolAdduct, self).get_id()

    def __str__(self):
        return "{}({})".format(self.get_id(),str(self.adduct))

def par_sibmol(x):
    try:
        return (sibMol(x),True)
    except Exception:
        return (None,False)

#todo leavbe only one of the 2 functions
def build_sibmols(inputs,remove_incorrect=True,parallel = True):
    RDLogger.DisableLog('rdApp.*') 
    if parallel:
        with mp.Pool(mp.cpu_count()) as p:
            res_list = p.map(par_sibmol,inputs)
    else:
        res_list = [par_sibmol(input) for input in inputs]
    RDLogger.EnableLog('rdApp.*')
    return res_list


def buildSibMols(inputs,remove_incorrect=True):
    if isinstance(inputs,Series):
        inputs = inputs.to_list()
    if isinstance(inputs,list):
        return build_sibmols(inputs,remove_incorrect=remove_incorrect)
    else:
        raise TypeError("'inputs' should be a list or a pandas.Serie with valid SMILES or InChi.")

