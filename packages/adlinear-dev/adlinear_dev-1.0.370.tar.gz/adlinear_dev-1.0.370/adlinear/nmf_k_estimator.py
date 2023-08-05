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


class NCompEstimator:

    def __init__(self):
        pass

    def estimate_ncomp(mat: Union[pd.DataFrame, np.ndarray]):

        ncmin = 2
        ncmax = 35
        df_screeplot = nmfmodel.generate_scree_plot(mat, 2, 35)
        df_mini_scree_plots = pd.DataFrame(index=[], columns=[])
        df_mini_scree_plots = nmfmodel.collect_windows_from_scree_plot(df_collected_windows=df_mini_scree_plots,
                                                                       df_scree_plot=df_screeplot,
                                                                       window_size=6)

        return

    pass
