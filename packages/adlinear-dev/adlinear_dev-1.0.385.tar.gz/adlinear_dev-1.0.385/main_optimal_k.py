import numpy as np
import pandas as pd
import adinference
from adinference import admlp
from adlinear import utilities as utl
from adlinear import nmf_k_estimator as ke
import root_path
from transparentpath import Path
import os
import dotenv
from randomgenerators import randomgenerators as rng


dotenv.load_dotenv()

if __name__ == "__main__":

    # Data localization
    rootpath = root_path.get_root_path()

    rd_path = Path(rootpath, fs="local") / os.getenv("rd_subpath")
    optimal_k_path: Path = Path(rd_path / os.getenv("optimal_k_subpath"), fs="local")

    data_path: Path = Path(optimal_k_path, fs="local") / os.getenv("data_subpath")
    models_path: Path = Path(optimal_k_path, fs="local") / os.getenv("models_subpath")

    temp_data_path = Path(data_path, fs="local") / "temp_data/"
    pictures_path = Path(data_path, fs="local") / "plot"
    out_data_path = Path(optimal_k_path, fs="local") / "results/"
    optk_model_dir = os.getenv("optk_model_dir", "model_MLP_p82")

    res_path = Path(optimal_k_path, fs="local") / os.getenv("results_subpath")

    raw_screeplots_filename: str = os.getenv("raw_screeplot_file")

    df_raw_screeplots: pd.DataFrame = (Path(data_path, fs="local") / raw_screeplots_filename).read(index_col=0)
    df_train = df_raw_screeplots.drop([col for col in df_raw_screeplots.columns if col.find("comp") >= 0],
                                      axis='columns', inplace=False)
    df_train = df_train.drop([col for col in df_train.columns if col.find("entropy") >= 0],
                             axis='columns', inplace=False)
    train_file_path = Path(data_path, fs="local") / "screeplots.csv"
    train_file_already_saved = True
    if not train_file_already_saved:
        train_file_path.write(df_train)

    mymlp = adinference.admlp.AdMlp(models_path, "model_MLP_p82")
    mymlp.load_model()

    my_k_estimator = ke.NCompEstimator(inference_model=mymlp)

    est_do_random_matrix = False
    if est_do_random_matrix:
        nb_clusters = 10
        h_size = 50
        h_avg = int(h_size / nb_clusters)
        w_size = 1000
        w_avg = int(w_size / nb_clusters)
        icorrmin = 0.80
        icorrmax = 0.99
        xcorrmin = 0.01
        xcorrmax = 0.30

        mat, _, _, _ = rng.generate_nmf_reconstruction(n_comp=nb_clusters, n_feat=h_size, n_obs=w_size,
                                                       avg_w_clust=w_avg, avg_h_clust=h_avg,
                                                       h_icorr_min=icorrmin, h_xcorr_max=xcorrmax,
                                                       w_icorr_min=icorrmin, w_xcorr_max=xcorrmax)
        preds = my_k_estimator.estimate_ncomp(mat=mat)
    est_do_train_data = False
    if est_do_train_data:
        train_data = df_raw_screeplots.drop(['Position'], axis="columns", inplace=False)
        # norm_train_data, _, _ = utl.normalize_by_columns(train_data, make_positive=False)
        norm_train_data = train_data.copy()
        norm_train_data.loc[:, "Tried_ncomp_0"] = train_data.loc[:, "Tried_ncomp_0"]
        norm_train_data = norm_train_data.iloc[0:16]
        ncmin = np.min(norm_train_data.index)
        ncmax = np.max(norm_train_data.index)-1
        train_synthegram = my_k_estimator.estimate_ncomp(df_mini_screeplots=norm_train_data, ncmin=ncmin, ncmax=ncmax)

    est_do_swimmer = True
    if est_do_swimmer:
        swimmer_file = "swimmer.xlsx"
        swimmer_data = pd.read_excel(str(data_path.path) + "/" + swimmer_file)
        swimmer_data = swimmer_data.iloc[:, 2:]
        swimmer_synthegram = my_k_estimator.estimate_ncomp(mat=swimmer_data, ncmin=2, ncmax=30)
        pass


