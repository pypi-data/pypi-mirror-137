from abc import ABC,abstractmethod

# Similarity class
class Similarity(ABC):
    def __init__(self,name,type):
        self.type = type
        self.name = name

    def preprocess(self,*obj):
        return obj[0]

    def __getitem__(self, item):
        o1,o2 = item
        if not isinstance(o1,self.type) and isinstance(o2,self.type):
            raise TypeError("Arguments should both be of type "+type.__str__())
        o1 = self.preprocess(o1)
        o2 =self.preprocess(o2)
        return self.computeSimilarity(o1,o2)

    @abstractmethod
    def computeSimilarity(self,o1,o2):
        raise ValueError("computeSimilarity needs to be implemented.")

class CachedSimilarity:
    def __init__(self,similarity):
        if not isinstance(similarity,Similarity):
            raise TypeError("'similarity' should be a similarity")
        else:
            self.similarity = similarity
        self.cache_id = {}
        self.cache = {}

    @abstractmethod
    def compute_key(self,obj):
        pass

    def get_index(self,okey):
        if okey in self.cache_id:
            return self.cache_id[okey]
        self.cache_id[okey] = len(self.cache_id)
        return self.cache_id[okey]


    def computeSimilarity(self,o1,o2):
        ikey1 = self.compute_key(o1)
        ikey2 = self.compute_key(o2)
        key1 = self.get_index(ikey1)
        key2 = self.get_index(ikey2)

        if key1>key2:
            ckey = (key2,key1)
        else:
            ckey = (key1,key2)

        s1,s2 = ckey
        if s1 in self.cache:
            tdict = self.cache[s1]
            if s2 in tdict:
                return tdict[s2]
            else:
                val = self.similarity.computeSimilarity(o1,o2)
                tdict[s2] = val
                return val
        else:
            val = self.similarity.computeSimilarity(o1,o2)
            self.cache[s1] = {s2:val}
            return val



# # Expanded similarity
# class ExpandedSimilarity:
#     def __init__(sim):
#
