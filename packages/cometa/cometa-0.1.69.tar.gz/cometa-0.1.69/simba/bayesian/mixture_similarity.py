import simba.bayesian.estimate_betamix as sbeta
from scipy.stats import beta
import simba.constants as COMMON
import logging
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import numpy as np



def get_estimators(name="beta"):
    if name=="beta":
        return BetaEstimator
    else:
        logging.warning("Incorrect similarity distributions: "+name+" using beta by default.")
        return BetaEstimator

##Beta distribution wrapper
def fit_beta(similarities,p=0.1, true=0.95,false=0.05,steps=1000, tolerance=0.001,initial_variance = 0.02):
    ab = [sbeta.ab_from_mv(true,initial_variance),sbeta.ab_from_mv(false,initial_variance)]
    pi = [p,1-p]
    init = (ab,pi)
    (ab, pi, usedsteps) = sbeta.estimate_mixture(similarities, init, steps=steps, tolerance=tolerance)
    return (ab, pi, usedsteps)


class ProbEstimator:
    def __init__(self, name,p=0.1, true = 0.5,false=0.2):
        self.p=p
        self.true = true
        self.false= false
        self.pi = []
        pass

    def compute_density_component(self,values,index,mixture=True):
        pass

    def fit(self,similarities,tolerance,steps):
        pass

    def compute_membership(self,similarities):
        pass

    def plot(self):
        labels = ["True","False"]
        if len(self.pi)==0:
            raise ValueError("Impossible to print distribution before it was fit")
        xseq = np.linspace(0.001,0.999,200)
        total_prob = None
        plt.xlim(0,1)
        for icomp in range(len(self.pi)):
            prob= self.compute_density_component(xseq,icomp,mixture=True)
            if total_prob is None:
                total_prob = prob
            else:
                total_prob += prob
            plt.plot(xseq,prob,label=labels[icomp])
        plt.plot(xseq,total_prob)
        plt.legend(loc="best")


class BetaEstimator(ProbEstimator):
    def __init__(self,**kwargs):
        super(BetaEstimator, self).__init__(name="beta", **kwargs)

    def fit(self,similarities,tolerance=0.001,steps=1000):
        ab,pi,usedsteps = fit_beta(similarities,p=self.p, true=self.true,false=self.false, steps=steps, tolerance=tolerance,initial_variance=0.02)
        self.ab=ab
        self.pi = pi

    def compute_density_component(self,values,index,mixture=True):
        factor = 1
        if mixture:
            factor = self.pi[index]
        return factor*beta.pdf(values,a=self.ab[index][0],b=self.ab[index][1])

    def compute_membership(self,similarities):
        mtrue = self.compute_density_component(similarities,index=0)
        mfalse = self.compute_density_component(similarities,index=1)
        total_prob = mtrue+mfalse
        mtrue=mtrue/total_prob
        mfalse=mfalse/total_prob
        return np.column_stack((mtrue,mfalse))


def get_true_probability(values,num_unique):
    estimator=get_estimators("beta")
    pprob = num_unique/len(values)
    mixed = estimator(p=pprob,true=max(values),false=min(values))
    mixed.fit(values)
    return mixed.compute_membership(values)[:,0]


if __name__=="__main__":
    from scipy.stats import beta
    import numpy as np
    m1 = 0.8
    m2 =0.2
    v1 = 0.02
    v2 = 0.02
    p = 0.2
    n = 1000
    a1,b1 = sbeta.ab_from_mv(m1,v1)
    a2,b2 = sbeta.ab_from_mv(m2,v2)
    s1 = beta.rvs(size=int(n*p),a=a1,b=b1)
    s2 = beta.rvs(size=int(n*(1-p)),a=a2,b=b2)
    similarities = np.concatenate([s1,s2])
    np.random.shuffle(similarities)
    xseq = np.linspace(0.001,0.999,500)
    density = gaussian_kde(similarities)
    plt.plot(xseq,density(xseq))
    plt.show()

    d1 = p*beta.pdf(xseq,a=a1,b=b1)
    d2 = (1-p)*beta.pdf(xseq,a=a2,b=b2)
    plt.plot(xseq,d1,label="True")
    plt.plot(xseq,d2,label="False")
    total = d1+d2
    plt.plot(xseq,total,label="Total")
    plt.legend()
    plt.xlim(0,1)
    plt.show()


    #
    estimator=get_estimators("beta")
    mixed = estimator(p=0.5,true=0.99,false=0.01)
    mixed.fit(similarities)
    mixed.compute_membership(similarities)
    mixed.plot()
