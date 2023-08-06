import pandas as pd
from simba.utils import matching
import logging
import simba.constants as const



def find_column(columns,authorized_terms,name):
    low_columns = [x.lower() for x in list(columns)]
    index = None
    for term in authorized_terms:
        term = term.lower()
        try:
            index = low_columns.index(term)
            break
        except ValueError:
            continue
    if index is None:
        raise KeyError("Impossible to find '"+name+"' column, authorized names are "+",".join(authorized_terms))
    return index


def find_colums(columns,authorized_prefixes,name):
    low_columns = [x.lower() for x in list(columns)]
    correct = [False]*len(low_columns)
    for term in authorized_prefixes:
        term = term.lower()
        for idx,cname in enumerate(low_columns):
            if correct[idx]: continue
            correct[idx]=cname.startswith(term)
    ##Return all the correct indexs
    indices = [idx for idx,corr in enumerate(correct) if corr]
    if len(indices)==0:
        raise KeyError("Impossible to find '"+name+"' column starting by one of: "+",".join(authorized_prefixes))
    return indices

def find_mz_column(columns):
    return find_column(columns,const.MZ_TERM,"mass")

def find_rt_column(columns):
    return find_column(columns,const.RT_TERM,"retention time")

def find_intensities(columns,supp_prefix=None):
    refs = const.INT_PREFIXES
    if supp_prefix is not None:
        refs = refs + [supp_prefix]
    return find_colums(columns,refs,"quantitative information")

class MsFeatures:
    def __init__(self,features,rt_unit = None,quant_prefix = None):

        #We check the rt_unit argument
        if rt_unit is not None:
            if rt_unit in const.RT_UNIT_MIN:
                logging.info("Retention time unit spotted 'minute'. (You can change it using the rt_unit argument)")
            elif mz_unit in const.RT_UNIT_SEC:
                logging.info("Retention time unit spotted 'second'. (You can change it using the rt_unit argument)")
            else:
                raise ValueError("unknown value of rt_unit:"+rt_unit+". Authorized values are "+const.RT_UNIT_MIN+","+const.RT_UNIT_SEC)

        self.features = features.copy(deep=True)
        self.mzidx = find_mz_column(features.columns)
        self.rtidx = find_rt_column(features.columns)
        self.intidx = find_intensities(features.columns,quant_prefix)

        # We check if the unit is minutes or
        mrt = self.rt()
        if rt_unit is None:
            if mrt.max()<90:
                logging.info("Retention time unit guessed 'minute'. (You can change it using the rt_unit argument)")
                rt_unit = const.RT_UNIT_MIN
            else:
                logging.info("Retention time unit guessed 'minute'. (You can change it using the rt_unit argument)")
                rt_unit = const.RT_UNIT_SEC

        #We convert the retention time in minut in every case
        if rt_unit == const.RT_UNIT_SEC:
            self.features[self.features.columns[self.rtidx]] = self.features[self.features.columns[self.rtidx]]/60

        self.mass_range = (min(self.mz()),max(self.mz()))

    def mz_range(self):
        return self.mass_range

    def mz(self):
        return self.features[self.features.columns[self.mzidx]]

    def rt(self):
        return self.features[self.features.columns[self.rtidx]]

    def mean_intensity(self):
        return self.intensities().mean(axis = 1,skipna=True)

    def count(self):
        return self.features.count()

    def intensities(self):
        return self.features[self.features.columns[self.intidx]]

    def unknown_idx(self):
        return len(self)

    def __getitem__(self,key):
        return self.features.iloc[key]


    def __len__(self):
        return len(self.features.index)


if __name__=="__main__":
    if False:
        PATH_FEATURES = "/home/dalexis/Documents/dev/LCMSBiolGen/data/processed/EcolK12Metabolites_full_lcms.csv"
        features = pd.read_csv(PATH_FEATURES,index_col=False)
        import numpy.random
        import numpy

        NSUPP = 10
        sim_int = numpy.random.uniform(-0.05,1,(features.shape[0],NSUPP))
        sim_int[sim_int<0] = numpy.nan
        for idx in range(NSUPP):
            fname = "Intensity_"+str(idx+1)
            features[fname]=sim_int[:,idx]

        mf = MsFeatures(features)
        aa= mf.rt()
        aa.max()
        mf.mean_intensity()
        mf.intensities()
