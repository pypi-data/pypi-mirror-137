from abc import ABC,abstractmethod

"""
The __init__ function just store the required parameters and check their types.
The initialize function use an existing annotation object and initializae all the required data structures. 
"""

class AnnotationLink(ABC):
    @abstractmethod
    def initialize(self,annotation):
        """Initialize a link object uysing an existing annotation"""
        pass
    @abstractmethod
    def get_probs(self,feat,cands,annotation):
        """Get the probabilty of feature given candidates"""
        pass

    @abstractmethod
    def update_annotation(self,feat,old_annot,new_annot):
        """Update the probablity of annotation"""
        pass

    @abstractmethod
    def unknown_prob(self):
        """Probability of unknown compounds"""
        pass
