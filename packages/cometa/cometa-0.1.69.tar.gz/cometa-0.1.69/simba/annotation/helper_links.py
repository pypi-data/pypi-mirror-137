import logging
from simba.utils import matching

from simba.annotation.links.chemsim import ChemicalSimilarityLinks
from simba.annotation.links.gem import GemLinks
from simba.annotation.links.adducts import AdductsLinks
from simba.annotation.links.homologous import HomologousLinks
from simba.annotation.links.msms_network import NetworkMSMSLinks

_LINK_DICT = {
    "pathway":ChemicalSimilarityLinks,
    "bio":ChemicalSimilarityLinks,
    "biological":ChemicalSimilarityLinks,
    "reaction":ChemicalSimilarityLinks,
    "homologue":HomologousLinks,
    "homologuous":HomologousLinks,
    "homologuous serie":HomologousLinks,
    "chemical similarity":HomologousLinks,
    "adduct":AdductsLinks,
    "gem":GemLinks,
    "genome-scale model":GemLinks,
    "gnps-network":NetworkMSMSLinks,
    "msms-network":NetworkMSMSLinks
}


#This function return the links
def get_link(name:str):
    """Find an 'AnnotationLinks' class given a name. Partial matches are allowed.
    You can find the list of the allowed keys by calling 'valid_links'.
    Args:
        name (str): The name to search for.

    Raises:
        ValueError: Raised in the name cannot be matche even approximately to the available links.

    Returns:
        The class associated to the AnnotationLinks NOT an instance 
    """
    name = name.lower()
    link = _LINK_DICT
    ratio,key = matching.match_string(name,list(link.keys()))
    if ratio<0.5:
        raise ValueError("Unknown key :"+name)
    if key!=name:
        logging.warning("Unknown key:"+name+" closest match used is:"+key)
    val_link = link[key]
    return val_link

def valid_links():
    """Return a list of the valid AnnotationLink key.

    Returns:
        List: A list of valid name for the 'get_links' function.
    """
    return list(_LINK_DICT.keys())
