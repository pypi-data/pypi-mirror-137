import pandas as pd
import adinference
# from adlinear import utilities as utl
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
    train_file_path.write(df_train)

    mymlp = adinference.admlp.AdMlp(models_path, optk_model_dir)
    mymlp.load_model()

    my_k_estimator = ke.NCompEstimator

    nb_clusters = 10
    h_size = 50
    w_size = 1000
    icorrmin = 0.80
    icorrmax = 0.99
    xcorrmin = 0.01
    xcorrmax = 0.30

    mat, _, _, _ = rng.generate_nmf_reconstruction(n_comp=nb_clusters, n_feat=h_size, n_obs=w_size)
    my_k_estimator.estimate_ncomp(mat=mat)
    pass
