import logging
from simba.utils import matching
from simba.annotation.prior.structural_property import MassProperty, RtProperty, ThresholdedRtProperty
from simba.annotation.prior.ms2 import SiriusLink,GNPSLibraryLinks,AnnotationFlowLinks,MS2LinksCsv


_PRIOR_DICT = {"mass":MassProperty,
    "mz":MassProperty,
    "monoisotopic.mass":MassProperty,
    "rt":ThresholdedRtProperty,
    "rtime":ThresholdedRtProperty,
    "retention.time":ThresholdedRtProperty,
    "time":ThresholdedRtProperty,
    "raw_rt":RtProperty,
    "raw_rtime":RtProperty,
    "raw_retention.time":RtProperty,
    "raw_time":RtProperty,
    "thresholded_rtime":ThresholdedRtProperty,
    "gnps":GNPSLibraryLinks,
    "annotationflow":AnnotationFlowLinks,
    "ms2":MS2LinksCsv,
    "ms2csv":MS2LinksCsv,
    "sirius":SiriusLink
    }

def valid_priors():
    """Return a list of the valid AnnotationLink key.

    Returns:
        List: A list of valid name for the 'get_links' function.
    """
    return list(_PRIOR_DICT.keys())


def get_prior(name):
    """Find a 'PriorMatches' class given a name. Partial matches are allowed.
    You can find the list of the allowed keys by calling 'valid_priors'.
    Args:
        name (str): The name to search for.

    Raises:
        ValueError: Raised in the name cannot be matche even approximately to the available links.

    Returns:
        The class associated to the PriorLinks NOT an instance 
    """
    name = name.lower()
    ratio,key = matching.match_string(name,list(_PRIOR_DICT.keys()))
    if ratio<0.5:
        raise ValueError("Unknown key :"+name)
    if key!=name:
        logging.warning("Unknown key:"+name+" closest match used is:"+key)
    return _PRIOR_DICT[key]