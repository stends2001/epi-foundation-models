import pandas as pd 
from dataclasses import dataclass

from .utils import PathManager

pm = PathManager()

@dataclass 
class EpiConfig:
    """
    Task - configuration class.

    Parameters
    ----------
    disease : str
        Name of the disease, as saved in data.
    min_date : str
        Minimum date; the starte date of context data.
    split_date : str
        The start date of the test data.
    max_date : str
        The final date of the test data.

    Downstream
    ----------
    Data is loaded and processed based on ``EpiConfig``, inside ``BaseModel``.
    Models forecast based on the processed data.
    """

    disease : str 

    min_date : str
    split_date : str
    max_date : str

def load_data(cfg: EpiConfig) -> pd.DataFrame:
    """load raw data from expected path based on ``disease`` of ``EpiConfig``."""
    df_raw = pd.read_csv(pm.data / 'epidemiology' / (cfg.disease+".csv"))    
    return df_raw 

def process_data(df_raw: pd.DataFrame, cfg: EpiConfig) -> pd.DataFrame:
    """processes raw data based on ``EpiConfig``. Data is aggregated nationally, filtered on time, and grouped into context and test data."""    
    df_pcd = df_raw.copy()

    # aggregate to national case numbers
    df_pcd = df_pcd.groupby(['timestamp'])['cases'].sum().reset_index(drop = False)

    # set timestamp as datetime 
    df_pcd['timestamp'] = pd.to_datetime(df_pcd['timestamp'])    

    # set context and test columns
    df_pcd['context']   = ((df_pcd['timestamp'] >= cfg.min_date) & (df_pcd['timestamp'] < cfg.split_date))
    df_pcd['test']      = ((df_pcd['timestamp'] >= cfg.split_date) & (df_pcd['timestamp'] <= cfg.max_date)) 

    # remove other dates   
    df_pcd = df_pcd[df_pcd['timestamp'] < cfg.max_date]
    df_pcd = df_pcd[df_pcd['timestamp'] >= cfg.min_date]

    # set cases as int
    df_pcd['cases'] = df_pcd['cases'].astype(int)

    return df_pcd.reset_index(drop = True)