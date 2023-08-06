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
        preds = self._inference_model.predict(data_for_inference)
        return preds

    def estimate_ncomp(self, mat: Union[pd.DataFrame, np.ndarray],
                       ncmin: int = 2, ncmax: int = 35):

        df_screeplot = nmfmodel.generate_scree_plot(mat, ncmin=ncmin, ncmax=ncmax)
        df_mini_scree_plots = pd.DataFrame(index=[], columns=[])
        df_mini_scree_plots = nmfmodel.collect_windows_from_scree_plot(df_collected_windows=df_mini_scree_plots,
                                                                       df_scree_plot=df_screeplot,
                                                                       window_size=6)
        data_for_inference = df_mini_scree_plots.drop([col for col in df_mini_scree_plots.columns if
                                                       col.find("_ncomp") >= 0 or col.find("_entropy") >= 0
                                                       or col.find("Position") >= 0],
                                                      axis="columns", inplace=False).to_numpy(dtype=np.float64)

        preds = self.get_predictions(data_for_inference)
        return preds

    pass
