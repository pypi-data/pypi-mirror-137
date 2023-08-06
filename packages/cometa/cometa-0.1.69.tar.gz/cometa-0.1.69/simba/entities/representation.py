import os
import tempfile
from simba.io.storage import Storage

from simba.entities.molecule import sibMol

###import for Descriptors Image
from rdkit.Chem import Descriptors,RDKFingerprint,MACCSkeys,AllChem,MolFromSmiles
from rdkit.ML.Descriptors import MoleculeDescriptors
from rdkit.Chem import MolFromSmiles
import simba.constants as CONST

###import for Structural Fingerprints Image
from rdkit.Chem.AtomPairs import Pairs,Torsions

DEMO_MOL = MolFromSmiles("CC")

##SHOULD NOT BE INSTANSIATED
class MoleculeImage:
    def __init__(self,name):
        self.name=name
        pass

    def get_name(self):
        return self.name

    def represent(self,mol):
        pass

class MolecularDescriptors(MoleculeImage):
    descList = [dd[0] for dd in Descriptors.descList]
    calculator = MoleculeDescriptors.MolecularDescriptorCalculator(descList)

    def __init__(self):
        super(MolecularDescriptors, self).__init__(CONST.image_desc_name)

    def represent(self,mol):
        return MolecularDescriptors.calculator.CalcDescriptors(mol.rdmol())


def len_fingerprints(fg):
    if hasattr(fg,"GetLength"):
        return fg.GetLength()
    if hasattr(fg,"GetNumBits"):
        return fg.GetNumBits()
###A dictionnary of the non zero
def non_zero(fg):
    if hasattr(fg,"GetLength"):
        return fg.GetNonzeroElements()
    if hasattr(fg,"GetNumBits"):
        temp = list(fg.ToBitString())
        res = {idx:int(obj) for idx,obj in enumerate(temp) if obj != '0'}
        return res


class StructuralFingerprint(MoleculeImage):
    MAX_MORGAN = 5

    def __init__(self):
        self.fingerprinters = dict()
        super(StructuralFingerprint, self).__init__(CONST.image_finger_name)
        self.buildFingerprinters()
        self.len=None

    def get_max_morgan(self):
        return self.MAX_MORGAN

    def set_max_morgan(self,m):
        self.MAX_MORGAN = m

    def defaultFingerprints(self):
        default = {'RDK': RDKFingerprint,
                   'MACCS': MACCSkeys.GenMACCSKeys,
                   'PAIR': Pairs.GetHashedAtomPairFingerprint,
                   'TORSIONS': Torsions.GetHashedTopologicalTorsionFingerprint}
        return default

    def reduce_by_prefix(self,prefixes):
        all_names = list(RepresentationsDB.representations_index['struct-fingerprints'].fingerprinters.keys())
        if prefixes is None:
            prefixes = ["MORGAN_ECFP","MACCS"]
        new_name = [ff for pre in prefixes for ff in all_names if ff.startswith(pre)]
        new_fingerprinters = {nn:self.fingerprinters[nn] for nn in new_name}
        if len(new_fingerprinters)==0:
            raise KeyError("No structural fingerprints remaining. Aborting.")
        self.fingerprinters = new_fingerprinters

    def buildFingerprinters(self):
        ecfp_morgan = {("MORGAN_ECFP" + str(i)): lambda x, i=i: AllChem.GetHashedMorganFingerprint(x, i) for i in range(1, self.MAX_MORGAN)}
        fcfp_morgan = {("MORGAN_FCFP" + str(i)): lambda x, i=i: AllChem.GetHashedMorganFingerprint(x, i, useFeatures=True) for i in range(1, self.MAX_MORGAN)}
        default = self.defaultFingerprints()
        self.fingerprinters = {**ecfp_morgan,**fcfp_morgan,**default}

    def getFingerprinters(self):
        return self.fingerprinters

    def setFingerprinters(self,obj):
        self.fingerprinters=obj

    def represent(self,mol):
        smol = mol.rdmol()
        raw = [fingerprint(smol) for fingerprint in self.fingerprinters.values()]
        shift = 0
        final_dic = {}
        for rr in raw:
            temp = non_zero(rr)
            for key,val in temp.items():
                final_dic[(key+shift)] = val
            shift = shift+len_fingerprints(rr)
        return final_dic

    def __len__(self):
        return sum([len_fingerprints(fingerprint(DEMO_MOL)) for fingerprint in self.fingerprinters.values()])

# ##List of Descritpors
ImagesList = [MolecularDescriptors,StructuralFingerprint]

def build_representation(storage=None):
    if isinstance(storage,RepresentationsDB):
        return storage
    if storage is None:
        storage = tempfile.mkdtemp()
    return RepresentationsDB(storage)


class RepresentationsDB:
    ###A dictionnary
    representations_index = [img() for img in ImagesList]
    representations_index = {rr.get_name():rr for rr in representations_index}

    def __init__(self,path,save_interval=500):
        ###THE representation are always stored by dir
        self.path = path
        if path is not None:
            if not os.path.isdir(path):
                raise ValueError("Path impossible to create: "+path+".")
            storage_path = {name:self.generate_path(name) for name in RepresentationsDB.representations_index.keys()}
        else:
            storage_path = {name:None for name in RepresentationsDB.representations_index.keys()}
        self.storage = {name:Storage(path,save_interval=save_interval) for name,path in storage_path.items()}
        self.hash = str(sum([hash(rr) for rr in self.representations_index["struct-fingerprints"].fingerprinters.keys()]))[0:6]

    def generate_path(self,name):
        return os.path.join(self.path,name+".simdb")

    def reduce_structural_fingerprints(self,subset):
        self.representations_index[CONST.image_finger_name].reduce_by_prefix(subset)

    def get_fingerprints_size(self):
        return len(self.representations_index[CONST.image_finger_name])

    def get_representations(self):
        return list(RepresentationsDB.representations_index.keys())

    def __getitem__(self, idx):
        mol,type=idx
        key = mol.get_id()
        if not type in self.storage:
            raise KeyError(type," Image is not known, authorized representations are",self.get_representations())
        storage = self.storage[type]
        if key in storage:
            return storage[key]
        ###else we have to compute it
        computer = RepresentationsDB.representations_index[type]
        representation = computer.represent(mol)
        storage[key] = representation
        return representation
