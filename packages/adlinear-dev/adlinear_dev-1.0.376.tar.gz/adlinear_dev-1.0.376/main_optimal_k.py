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
    optimal_k_path: object = Path(rd_path / os.getenv("optimal_k_subpath"), fs="local")

    data_path: object = Path(optimal_k_path / os.getenv("data_subpath"), fs="local")
    models_path: object = Path(optimal_k_path / os.getenv("models_subpath"), fs="local")

    temp_data_path = Path(data_path / "temp_data/", fs="local")
    pictures_path = Path(data_path / "plot", fs="local")
    out_data_path = Path(optimal_k_path / "results/", fs="local")
    optk_model_dir = Path(models_path / os.getenv("optk_model_dir", "model_MLP_p82"), fs="local")

    res_path = Path(optimal_k_path / os.getenv("results_subpath"), fs="local")

    raw_screeplots_filename: str = os.getenv("raw_screeplot_file")

    df_raw_screeplots: pd.DataFrame = Path(data_path / raw_screeplots_filename, fs="local").read(index_col=0)
    df_train = df_raw_screeplots.drop([col for col in df_raw_screeplots.columns if col.find("comp") >= 0],
                                      axis='columns', inplace=False)
    df_train = df_train.drop([col for col in df_train.columns if col.find("entropy") >= 0],
                             axis='columns', inplace=False)
    train_file_path = Path(data_path / "screeplots.csv", fs="local")
    train_file_already_saved = True
    if not train_file_already_saved:
        train_file_path.write(df_train)

    mymlp = adinference.admlp.AdMlp(models_path, optk_model_dir)
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
    est_do_train_data = True
    if est_do_train_data:
        train_data = df_train.drop(['Position'], axis="columns", inplace=False)
        train_data, _, _ = utl.normalize_by_columns(train_data, make_positive=False)
        train_preds = my_k_estimator.get_predictions(train_data)
    pass
