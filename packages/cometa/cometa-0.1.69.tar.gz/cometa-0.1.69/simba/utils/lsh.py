import numpy as np
import logging
from scipy.spatial.distance import pdist,squareform
from simba.utils.parallel_extension import parallel_apply_along_axis
import tqdm
import itertools

def initialize_hyperplan(input_dim):
    return np.random.normal(size=input_dim)


class LSH:
    def __init__(self,hash_size,input_dim,windows=0.1,num_hash=3,plans=None):
        self.hash_size = hash_size
        self.input_dim = input_dim
        self.windows = windows

        if plans is not None:
            self.plans = plans
        else:
            self.plans = []
            for _ in range(num_hash):
                temp = [initialize_hyperplan(self.input_dim) for _ in range(hash_size)]
                self.plans.append(np.vstack(temp))
        self.num_hash = num_hash
        self.buckets = [dict() for _ in range(num_hash)]

    def _hash(self,elems,plans):
        vdots = np.einsum("ik,jk->ij",plans,elems)
        vdots = np.ceil(vdots/self.windows)
        hashes = np.apply_along_axis(lambda x:"|".join([str(int(i)) for i in x.tolist()]),0,vdots)
        return hashes.tolist()

    def store(self,points):
        self.points = points
        vids = [self._hash(points,plans) for plans in self.plans]
        vids = list(zip(*vids))
        for idx,hash in enumerate(vids):
            for hidx in range(self.num_hash):
                if hash[hidx] in self.buckets[hidx]:
                    self.buckets[hidx][hash[hidx]].append(idx)
                else:
                    self.buckets[hidx][hash[hidx]] = [idx]

    def neighbours(self,point):
        vhashes = [self._hash(point,plans) for plans in self.plans]
        # print(vhashes)
        # for chash,buck in zip(vhashes,self.buckets):
        #     print("\n")
        #     print((chash,buck))
        # print([(chash,buck) for chash,buck in zip(vhashes,self.buckets)])
        cneighbours = [buck[chash[0]] for chash,buck in zip(vhashes,self.buckets) if chash[0] in buck]
        if len(cneighbours)==0:
            return []
        return list(set(itertools.chain(*cneighbours)))

        # #We reduce the set
        # for hidx in range(self.num_hash):
        #     if hash in self.buckets[hidx]:
        #         self.buckets[hidx][hash].append(idx)
        #     else:
        #         self.buckets[hidx][hash] = [idx]
        # if vhash[0] not in self.buckets:
        #     return []
        # return self.buckets[vhash[0]]

    def nn(self,point,k):
        pidx = np.array(self.neighbours(point))
        if len(pidx)==0:
            return np.array([])
        points = self.points[pidx]
        ##We compute all the L2 distance
        vdist = np.linalg.norm(points-point)
        vneighbours = np.argsort(vdist)
        return pidx[vneighbours[0:min(k,len(vneighbours))]]
        ##We select the minimum point

    def nn_radius(self,point,radius):
        pidx = np.array(self.neighbours(point))
        if len(pidx)==0:
            return np.array([])
        points = self.points[pidx]
        ##We compute all the L2 distance
        # print(points-point)
        vdist = np.apply_along_axis(np.linalg.norm, 1, points-point)
        vneighbours = np.argsort(vdist)
        # print(vdist)
        # print(vneighbours)
        didx = 0
        while didx < len(vdist):
            if vdist[vneighbours[didx]]>radius:
                return pidx[vneighbours[0:didx]]
            didx += 1
        if didx != 0:
            return pidx
        return np.array([])
        ##We select the minimum point

    def nn_radius_points(self,points,radius):
        # def wrap_fun(point):
        #     self.nn_radius(point,radius)
        vval = [None]*(points.shape[0])
        for idx in tqdm.tqdm(range(points.shape[0])):
            vval[idx]=self.nn_radius(points[idx,:],radius=radius)
        return vval
        # return [self.nn_radius(points[idx,:],radius=radius) for idx in range(points.shape[0])]
        # return parallel_apply_along_axis(self.nn_radius, 1, points,radius=radius)

if __name__=="_main__":
    ll = LSH(3,5,windows=0.5)
    tdat = np.array([[1,2,3,4,5],[1,2.1,3,4,5],[1,2,3,4,5],[0,0,0,0,0],[-1,-2,-3,-4,-5]])
    ll.store(tdat)
    ll.buckets[0]

    ll.nn_radius(np.array([[1.01,2,3,4,5]]),1)

    vdots
    np.ceil(vdots/0.1)
    import itertools
    list(set(itertools.chain(*[[1.2,2],[1.2,4,5],[]])))
