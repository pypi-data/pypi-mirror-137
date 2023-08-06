import numpy as np


def build_limits(f,unknown_idx):
    ef = np.array(([-1]+f.tolist()+[unknown_idx]))
    #Borders of interval
    upper_lim = ef[2:]
    upper_lim = upper_lim.copy()
    lower_lim = ef[0:-2]+1
    lower_lim = lower_lim.copy()

    #Handling lower lim
    clower_lim = 0
    for idx in range(len(f)):
        if f[idx]==unknown_idx:
            lower_lim[idx] = clower_lim
        else:
            lower_lim[idx] = clower_lim
            clower_lim = f[idx]+1

    # Handling upper lim
    cupper_lim = unknown_idx
    for idx in range(len(f)-1,-1,-1):
        # print(idx,": ",cupper_lim)
        if f[idx]==unknown_idx:
            upper_lim[idx] = cupper_lim
        else:
            upper_lim[idx] = cupper_lim
            cupper_lim = f[idx]
    return lower_lim,upper_lim

def compute_jump_probability(old_ff,new_ff,probs=None):
    # print("\n\nnew\n:")
    num_y = probs.shape[-1]-1
    #We compute the extended sequence.
    ef = old_ff.copy()
    unknown_idx = probs.shape[1]-1
    #Borders of interval
    lower_lim,upper_lim = build_limits(old_ff,num_y)
    # print("lower_lim:",lower_lim)
    # print("upper_lim:",upper_lim)
    #Compute all the interval size
    rsize = upper_lim-lower_lim
    #Boolean for used features
    used = np.zeros(len(old_ff))
    forward_log_prob = 0
    for _ in range(len(old_ff)):
        #Pick the feature with the largest range
        osize = np.argsort(rsize)
        sel_idx = len(osize)-1
        while used[osize[sel_idx]]:
            sel_idx -= 1
        sel_idx = osize[sel_idx]
        used[sel_idx] = 1
        #We sample the new index
        sel_range = rsize[sel_idx]
        #If the range is 0 it can only be an unknown compound
        if (upper_lim[sel_idx]-lower_lim[sel_idx])<=0:
            ef[sel_idx]=unknown_idx
            continue
        # print("######")
        #print("sel_idx:",sel_idx,"ef:",ef,"lower_lim:",lower_lim,"upper_lim:",upper_lim,"rsize:",rsize)
        #We pick the uknonwn probability in every cases
        sprobs_idx = list(range((lower_lim[sel_idx]),(upper_lim[sel_idx])))+[unknown_idx]
        sel_probs = probs[sel_idx,sprobs_idx]
        #Probability of the correct features are extracted
        sel_probs = sel_probs/np.sum(sel_probs)
        temp_idx = new_ff[sel_idx]-lower_lim[sel_idx]
        if temp_idx>sel_range:
            temp_idx = sel_range
        if np.any(temp_idx<0):
            print(old_ff,new_ff,probs.shape)
        forward_log_prob += np.log(sel_probs[temp_idx])

        #We detemrine the new upper limit
        if temp_idx==sel_range:
            new_feature = unknown_idx
            new_lower = old_ff[sel_idx]+1
            new_upper = old_ff[sel_idx]
        else:
            new_feature = lower_lim[sel_idx]+temp_idx
            if old_ff[sel_idx]==unknown_idx:
                new_upper = new_feature
                new_lower = new_feature+1
            else:
                if new_feature>old_ff[sel_idx]:
                    new_upper = old_ff[sel_idx]
                    new_lower = new_feature+1
                elif new_feature<=old_ff[sel_idx]:
                    new_upper = new_feature
                    new_lower = old_ff[sel_idx]+1
        # if new_lower>(unknown_idx-1):
        #     new_lower = (unknown_idx-1)

        #We modify the neighbouring unknonwn if the new sample is not unknown
        #if new_feature != unknown_idx:
        #shift_idx = lower_lim[sel_idx]-new_lower
        temp_shift_idx = sel_idx+1
        while temp_shift_idx<len(old_ff):
            shift_idx = lower_lim[temp_shift_idx]-new_lower
            #We only change the limit if the chane is disponible
            if shift_idx<0:
                rsize[temp_shift_idx] = rsize[temp_shift_idx]+shift_idx
                lower_lim[temp_shift_idx] = new_lower
            if ef[temp_shift_idx]!=unknown_idx:
                break
            temp_shift_idx += 1

        #We modify the upper lim
        temp_shift_idx = sel_idx-1
        #shift_idx = upper_lim[sel_idx]-new_upper
        while temp_shift_idx>=0:
            shift_idx = upper_lim[temp_shift_idx]-new_upper
            if shift_idx>0:
                rsize[temp_shift_idx] = rsize[temp_shift_idx]-shift_idx
                upper_lim[temp_shift_idx] = new_upper
            if ef[temp_shift_idx]!=unknown_idx:
                break
            temp_shift_idx -= 1
        ef[sel_idx] = new_feature
    return forward_log_prob


##Test with numba
def sequence_rsampling(f,probs=None):
    # print("\n\nnew\n:")
    num_y = probs.shape[-1]-1
    #We compute the extended sequence.
    ef = f.copy()
    unknown_idx = probs.shape[1]-1
    #Borders of interval
    lower_lim,upper_lim = build_limits(f,num_y)
    #Compute all the interval size
    #Declaration fo rnumpy
    rsize = upper_lim-lower_lim
    # sel_idx = 0
    # osize = np.zeros(len(rsize))
    # sel_range - 0
    #Boolean for used features
    used = np.zeros(len(f))
    forward_log_prob = 0
    for _ in range(len(f)):
        #Pick the feature with the largest range
        osize = np.argsort(rsize)
        sel_idx = len(osize)-1
        while used[osize[sel_idx]]:
            sel_idx -= 1
        sel_idx = osize[sel_idx]
        used[sel_idx] = 1
        #We sample the new index
        sel_range = rsize[sel_idx]
        #If the range is 0 it can only be an unknown compound
        if (sel_range)<=0:
            ef[sel_idx]=unknown_idx
            continue
        #We pick the uknonwn probability in every cases
        sprobs_idx = list(range((lower_lim[sel_idx]),(upper_lim[sel_idx])))+[unknown_idx]
        sel_probs = probs[sel_idx,sprobs_idx]
        #Probability of the correct features are extracted
        sel_probs = sel_probs/np.sum(sel_probs)
        temp_idx = np.random.choice(list(range(sel_range+1)),p=sel_probs)
        forward_log_prob += np.log(sel_probs[temp_idx])

        #We determine the new upper limits
        if temp_idx==sel_range:
            new_feature = unknown_idx
            new_lower = f[sel_idx]+1
            new_upper = f[sel_idx]
        else:
            new_feature = lower_lim[sel_idx]+temp_idx
            if f[sel_idx]==unknown_idx:
                new_upper = new_feature
                new_lower = new_feature+1
            else:
                if new_feature>f[sel_idx]:
                    new_upper = f[sel_idx]
                    new_lower = new_feature+1
                elif new_feature<=f[sel_idx]:
                    new_upper = new_feature
                    new_lower = f[sel_idx]+1
        temp_shift_idx = sel_idx+1
        while temp_shift_idx<len(f):
            shift_idx = lower_lim[temp_shift_idx]-new_lower
            #We only change the limit if the chane is disponible
            if shift_idx<0:
                rsize[temp_shift_idx] = rsize[temp_shift_idx]+shift_idx
                lower_lim[temp_shift_idx] = new_lower
            if ef[temp_shift_idx]!=unknown_idx:
                break
            temp_shift_idx += 1

        #We modify the upper lim
        temp_shift_idx = sel_idx-1
        #shift_idx = upper_lim[sel_idx]-new_upper
        while temp_shift_idx>=0:
            shift_idx = upper_lim[temp_shift_idx]-new_upper
            if shift_idx>0:
                rsize[temp_shift_idx] = rsize[temp_shift_idx]-shift_idx
                upper_lim[temp_shift_idx] = new_upper
            if ef[temp_shift_idx]!=unknown_idx:
                break
            temp_shift_idx -= 1
        ef[sel_idx] = new_feature
    return ef,forward_log_prob

def p_theta(f,probs):
    return np.sum(np.log(probs[np.arange(len(f)),f]))

def isomers_MH(probs, theta0, num_iterations = 5000, burn_in=1000, last_only = False):
    samples = []
    tprobs = []
    accepted = 0
    for nit in range(num_iterations):
        thetan,jump_prob = sequence_rsampling(theta0,probs=probs)
        #jump_prob = compute_jump_probability(theta0,thetan,num_y,probs)
        back_jump_prob = compute_jump_probability(thetan,theta0,probs)
        #print("forward:",jump_prob,"back:",back_jump_prob)
        p_thetan = np.sum(np.log(probs[np.arange(len(thetan)),thetan]))
        p_theta0 = np.sum(np.log(probs[np.arange(len(theta0)),theta0]))
        r=np.exp(p_thetan+jump_prob)/np.exp(p_theta0+back_jump_prob)
        #print("r:",r)
        frand = np.random.rand()
        if frand<r:
            theta0 = thetan
            if nit>burn_in:
                if last_only:
                    samples = thetan
                else:
                    samples.append(thetan)
            accepted += 1
        else:
            if nit<burn_in:
                continue
        #samples.append(theta0)
    alpha = accepted/(num_iterations-burn_in)
    if len(samples)==0:
        return (theta0,0.0)
    return (samples,alpha)


if __name__=="__main__":
    import numpy as np
    C = 400
    F = 5
    N = 50
    Niter = 50
    Nburnin = 20
    for _ in range(N):
        f0 = np.random.choice(list(range(C)),size=F,replace=False)
        f0 = np.sort(f0)
        probs = np.random.rand(F*C).reshape((F,C))
        try:
            rr = isomers_MH(probs,f0,Niter,Nburnin,True)
        except Exception as e:
            print("f0:",f0)
            raise Exception("Error")
