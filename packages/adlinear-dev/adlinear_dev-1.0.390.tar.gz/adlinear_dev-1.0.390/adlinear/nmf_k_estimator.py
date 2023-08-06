import math
from . import nmfmodel
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
# from .utilities import *
from . import utilities as utl
from typing import Union, Tuple
from adinference import admlp


class NCompEstimator:

    def __init__(self, inference_model: admlp.AdMlp):
        self._inference_model = inference_model
        pass

    def get_predictions(self, data_for_inference: np.ndarray):
        normalizers = self._inference_model.get_normalization()
        add_csts = pd.DataFrame(normalizers.iloc[0, :])
        mult_csts = pd.DataFrame(normalizers.iloc[1, :])
        norm_data_for_inference, _, _ = utl.normalize_by_columns(data_for_inference,
                                                                 add_cst=add_csts, mult_cst=mult_csts)
        preds = self._inference_model.predict(norm_data_for_inference)
        return preds

    def estimate_ncomp(self, mat: Union[pd.DataFrame, np.ndarray] = [],
                       df_mini_screeplots=None, ncmin: int = 2,
                       ncmax: int = 35, voting: str = "max"):

        if df_mini_screeplots is None:
            df_screeplot = nmfmodel.generate_scree_plot(mat, ncmin=ncmin, ncmax=ncmax)
            df_mini_screeplots = pd.DataFrame(index=[], columns=[])
            df_mini_screeplots = nmfmodel.collect_windows_from_scree_plot(df_collected_windows=df_mini_screeplots,
                                                                          df_scree_plot=df_screeplot,
                                                                          window_size=6)
        data_for_inference = df_mini_screeplots.drop([col for col in df_mini_screeplots.columns if
                                                      col.find("_ncomp") >= 0 or col.find("_entropy") >= 0
                                                      or col.find("Position") >= 0],
                                                     axis="columns", inplace=False).to_numpy(dtype=np.float64)

        preds = pd.DataFrame(index=df_mini_screeplots.index, data=self.get_predictions(data_for_inference))
        synthegram = pd.DataFrame(index=df_mini_screeplots.index, columns=["Score"], data=0)
        for irow, idx in enumerate(df_mini_screeplots.index):
            tried_ncomp = df_mini_screeplots.loc[idx, "Tried_ncomp_0"]
            shifts = [np.argmax(preds.iloc[irow, :])] if voting == "max" else range(preds.shape[1])
            for shift in shifts:
                pred = preds.iloc[irow, shift]
                if shift == 0:
                    synthegram.loc[:tried_ncomp] += pred
                elif shift == 5:
                    synthegram.loc[tried_ncomp + 5:] += pred
                    pass
                else:
                    if tried_ncomp + shift <= synthegram.index[-1]:
                        synthegram.loc[tried_ncomp + shift] += 5 * pred
                    pass
        return synthegram, preds, df_mini_screeplots

    pass
