import pkg_resources

###THIS FILE CONTAINS THE CONSTANTS USED, NOTABLY THE NAMES
###Name used for the rest of this shit
image_desc_name = "pc-descriptors"
image_finger_name = "struct-fingerprints"

###Name of the structural property
struct_prop_mass = "monoisotopic-mass"
struct_prop_rt = "retention-time"

###Name of the MS-MS similarities
sim_msms_cosine = "cosine-similarity"
sim_msms_double_cosine = "double-cosine-similarity"

###Name of the cosine moelcular similarities
sim_mol_dice = "dice-similarity"
sim_mol_tanimoto = "tanimoto-similarity"

###Data used to simulate to the data
path_model_biological = pkg_resources.resource_filename('simba', 'data/models/biological_link_new')
path_chebi = pkg_resources.resource_filename('simba', 'data/chebi.csv')
size_fingerprint_biological = 2048

###Mass term
MZ_TERM = ["mass","mz","monoisotopic.mass","m/z","m.z","mass-to-charge","mass.to.charge"]
RT_TERM = ["rt","rtime","retention.time","time"]
RT_UNIT_MIN = "minutes"
RT_UNIT_SEC = "seconds"
INT_PREFIXES = ["int","count"]

###Similarity modelling
MATCHING_DISTRIBUTIONS = ["beta"]

###Some rdkit constant
rdkit_num_atoms = 119
MASS_ELECTRON = 5.485799*1e-4

#Polarity handling part
POS = "positive"
NEG = "negative"

PRIOR = "prior"
PRIOR_SUPP = "sprior"
UNKNOWN_PROB = "unknown_prob"


def parse_polarity(x):
    x = x.lower()
    if isinstance(x,int):
        if x == 1:
            return POS
        if x == -1:
            return NEG
        else:
            raise ValueError("Impossible value to parse for polarity: "+str(x))

    if isinstance(x,str):
        if "pos" in x:
            return POS
        else:
            return NEG


main_adducts_pos = ["[M+H]+","[M+Na]+","[M-H2O+H]+","[M+NH4]+","[M-NH3+H]+"]
supp_adducts_pos = ["[M+H]+","[M+Na]+","[2M+H]+","[M+2H]2+","[M+Na+H]2+","[M-H2O+H]+","[M+NH4]+","[M-NH3+H]+"]
main_adducts_neg = ["[M-H]-","[M+CH3COOH-H]-","[M+Cl]-"]
supp_adducts_neg = ["[M-H]-","[M+CH3COOH-H]-","[M+Cl]-","[M-2H]2-","[2M-H]-"]


##OUTPUT
# These constants are only used to save the data.
SAVE_CANDIDATES = "candidates.pickle"
SAVE_FEATURES = "features.pickle"
SAVE_GA = "GA.pickle"
