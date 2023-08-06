from simba.utils import matching
from scipy.stats import norm,t
import logging

DEF_V = 0.01


DIC_DISTRIBUTION = {
    "normal":norm,
    "gaussian":norm, # loc = 0 is the mean and scale is the standard eviation
    "t":t} # Arguement df the degree of freedome

def determine_params_t(sigma):
    v = DEF_V
    return {"df":v}
def determine_params_norm(sigma):
    return {"loc":0,"scale":sigma}
#Just an alias
determine_params_gaussian = determine_params_norm

#All the distribution will be cnetered in 0
def get_distribution(name,sigma):
    if sigma<0:
        raise ValueError("Impossible to perform with a standard deviation of this shit.")
    name = name.lower()
    ratio,key = matching.match_string(name,list(DIC_DISTRIBUTION.keys()))
    if ratio<0.5:
        raise ValueError("Unknown distriubtion name given :"+name)
    if key!=name:
        logging.warning("Unknown key:"+name+" closest match used is:"+key)
    target_dist = key
    func_param = "determine_params_"+key
    args = eval(func_param+"(sigma)")
    target_dist = DIC_DISTRIBUTION[key](**args)
    return target_dist


if __name__ == "__main__":
    aa = get_distribution("gaus",sigma=56)
    bb = get_distribution("t",sigma=8)
    aa(1000)
    bb(1000)
