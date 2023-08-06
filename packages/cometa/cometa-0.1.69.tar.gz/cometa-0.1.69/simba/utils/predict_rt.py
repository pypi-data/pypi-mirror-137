
from simba.entities.molecule import sibMol
from simba.entities.representation import RepresentationsDB
import numpy as np
import xgboost as xgb


def get_rt_prediction_model(mols,rts,representations=None):
    sel_pos = [idx for idx,mol in enumerate(mols) if isinstance(mol,sibMol)]
    rts_sel = [rts[idx] for idx in sel_pos]
    sel_mols = [mols[idx] for idx in sel_pos]
    if representations is None:
        representations = RepresentationsDB(path=None,save_interval=None)
    all_fingerprints = [representations[sibMol(mol),"pc-descriptors"] for mol in sel_mols]
    descriptors = np.vstack(all_fingerprints)
    xgbm = xgb.XGBRegressor(n_estimators=20)
    xgbm = xgbm.fit(descriptors,rts_sel)
    return xgbm