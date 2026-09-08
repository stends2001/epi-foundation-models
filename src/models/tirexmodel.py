import torch 
import pandas as pd 
from tqdm import tqdm
import numpy as np

from tirex import ForecastModel, load_model


class TiRexModel:
    
    def __init__(self,
                 df: pd.DataFrame):
        
        modelcolor = 'darkgreen'
        modelname  = 'tirex'
        self.model: ForecastModel = load_model("NX-AI/TiRex", backend="torch") #type: ignore

        self.task = df

