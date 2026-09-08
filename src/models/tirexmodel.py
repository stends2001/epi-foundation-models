import torch 
import pandas as pd 
import numpy as np

from tirex import ForecastModel, load_model

from .basemodel import BaseModel
from ..dataloading import EpiConfig

class TiRexModel(BaseModel):
    """
    TiRexModel.

    Parameters
    ----------
    epicfg : EpiConfig
        Task - configuration class.

    Methods 
    -------
    ``forecast()``
        Makes model predictions.

    See Also
    --------
    ``BaseModel``
        The parent class of all models, that contains shared model behavior.
    ``EpiConfig``
        Task - configuration class.    

    Downstream
    ----------
    A model subclass like ``TiRexModel`` is called with ``EpiConfig``, and prepares data in itself.
    Model predictiosn are made thorugh ``forecast()`` and visualized through ``plot_preds()``.

    Examples
    --------
    >>> cfg1 = EpiConfig(
    ...    'campylobacter',
    ...    '2002-01-01',
    ...    '2024-01-01',
    ...    '2025-01-01'
    ...    )

    ... tirex1 = TiRexModel(cfg1)
    ... tirex1.forecast()

    ... fig1 = tirex1.plot_split()
    ... fig2 = tirex1.plot_preds(False) 
    """

    
    def __init__(self,
                 epiconfig: EpiConfig):
   
        modelname  = 'tirex'
        modelcolor = "#1b9e77"

        self.model: ForecastModel = load_model("NX-AI/TiRex", backend="torch") #type: ignore

        super().__init__(modelname, modelcolor, epiconfig)

    def forecast(self):
        """Make model predictions, stored into ``predictions``."""
        predictions_quantiles: torch.Tensor
        predictions_mean: torch.Tensor

        number_predictions = len(self.test_data)

        context_tensor = torch.tensor(self.context_data['cases'].values,    dtype = torch.float32).unsqueeze(0)

        predictions_quantiles, predictions_mean = self.model.forecast(context = context_tensor,prediction_length = number_predictions) # type: ignore

        # reshape:
        predictions = self._reshape_preds(predictions_quantiles, predictions_mean)

        # add targets:
        predictions = pd.merge(self.test_data, predictions, left_index=True, right_index=True)

        self.predictions = predictions

    def _reshape_preds(self, 
                       quantiles: torch.Tensor, 
                    mean: torch.Tensor):
        """format model predictions from torch.tensor into a pd.dataframe."""
        
        mean_np         = mean.detach().cpu().numpy().transpose()
        quantiles_np    = quantiles.squeeze(0).detach().cpu().numpy()

        quantiles_lbls  = ['pred',
            'pred_q1', 'pred_q2', 'pred_q3', 
            'pred_q4', 'pred_q5', 'pred_q6', 
            'pred_q7', 'pred_q8', 'pred_q9'
        ]

        df = pd.DataFrame(
            np.column_stack([mean_np, quantiles_np]),
            columns=quantiles_lbls 
        )

        return df   