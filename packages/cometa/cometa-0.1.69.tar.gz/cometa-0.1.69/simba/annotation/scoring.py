import numpy as np

def get_scorer(x):
    if x=="sigmoid":
        return build_sigmoid
    if x=="dirichlet":
        return build_dirichlet


def build_sigmoid(shift=1,alpha=1):
    def tsigmoid(x):
        return shift/(shift+np.exp(-alpha*x))
    return tsigmoid

# A cached scorer for commodity purpose.
class DiscreteScorer:
    def __init__(self,fun,val_max=1000):
        self.fun = fun
        self.tabval = np.array([fun(x) for x in np.arange(val_max+1)])
    def __call__(self,val):
        return self.tabval[val]

def build_dirichlet(delta,total_cand):
    def tdirichlet(x):
        return (x+delta)/(total_cand*delta+np.sum(x))

#Pair scoring
def exp_pair(ti,tj,sigma):
    return exp_diff(ti-tj,sigma)

def exp_diff(diff,sigma):
    return np.exp(-diff**2/(2*sigma**2))