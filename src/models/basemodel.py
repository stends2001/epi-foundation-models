import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns

from ..dataloading import load_data, process_data, EpiConfig

class BaseModel:
    """
    Parent class of all models, not to be called in itself.

    Parameters
    ----------
    model_name : str
        Name of the model.
    model_color : str
        Color of the model, shown in forecasts.
    epicfg : EpiConfig
        Task - configuration class.

    Methods 
    -------
    ``_prepare_data()``
        Prepare data for models to be able to forecast.
    ``forecast()``
        Method to create predictions in ``.predictions``. To be defined in child class.
    ``plot_splits()``
        Plot context and test data.
    ``plot_preds()``
        Plot model predictions.    
    """

    def __init__(self,
                 model_name : str,
                 model_color : str,
                 epicfg : EpiConfig):

        self.modelcolor     = model_color 
        self.modelname      = model_name

        self.contextcolor   = '#4a90d9' 
        self.testcolor      = '#d94e4e'    

        self.epicfg         = epicfg

        self.context_data, self.test_data = self._prepare_data()
        self.predictions: pd.DataFrame | None = None

    def forecast(self):
        raise NotImplementedError('Each model childclass should have a ``forecast()`` method implemented.')

    def _prepare_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """orchestrates dataloading and processing."""
        df_raw = load_data(self.epicfg)
        df_pcd = process_data(df_raw, self.epicfg)         

        ctx = df_pcd[df_pcd['context']].reset_index(drop=True)
        tst = df_pcd[df_pcd['test']].reset_index(drop=True)
        return ctx, tst                     

    def plot_split(self):
        """plot context vs test data"""
        title = f'{self.epicfg.disease.capitalize()} - weekly cases in Germany'

        fig, ax = plt.subplots(1,1,figsize = (10,4))
        sns.lineplot(self.context_data, x = 'timestamp', y = 'cases',  color = self.contextcolor, label = 'context', ax = ax)
        sns.lineplot(self.test_data,    x = 'timestamp', y = 'cases',  color = self.testcolor,    label = 'test', ax = ax)


        ax.legend(loc = 'upper left')
        ax.set_title(title, loc = 'left', fontweight = 'bold')
        ax.set_xlabel("")
        ax.set_ylabel("Cases")

        ymax = max(self.test_data['cases'].max(), self.context_data['cases'].max())

        ax.set_ylim([-0.01 * ymax, 1.01 * ymax]) # type: ignore

        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_visible(True)        
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)             
        return fig

    def plot_preds(self, context : bool):
        """plot modelpredictions with or without context data."""

        if self.predictions is None:
            raise ValueError(f'Predictions doesnt exist on {self.modelname}. Forecast first!')

        title = f'Predictions {self.epicfg.disease.capitalize()} - weekly cases in Germany'

        if context:

            fig, ax = plt.subplots(1,1,figsize = (10,4))
            sns.lineplot(self.context_data, x = 'timestamp', y = 'cases',  color = self.contextcolor, label = 'context', ax = ax)
            ymax = max(self.test_data['cases'].max(), self.context_data['cases'].max(), self.predictions['pred_q9'].max())

        else: 

            fig, ax = plt.subplots(1,1,figsize = (7,4))
            ymax = max(self.test_data['cases'].max(), self.predictions['pred_q9'].max())

        sns.lineplot(self.test_data,  x = 'timestamp', y = 'cases',  color = self.testcolor,    label = 'test',ax = ax)    
        sns.lineplot(self.predictions,  x = 'timestamp', y = 'pred',   color = self.modelcolor, label = 'predictions', ax = ax)

        

        ax.fill_between(
                        x       = self.predictions['timestamp'],
                        y1      = self.predictions['pred_q1'],
                        y2      = self.predictions['pred_q9'],
                        color   = self.modelcolor,
                        alpha   = 0.2
                    )        


        ax.legend(loc = 'upper left')
        ax.set_title(title, loc = 'left', fontweight = 'bold')
        ax.set_xlabel("")
        ax.set_ylabel("Cases")


        ax.set_ylim([-0.01 * ymax, 1.01 * ymax])  # type: ignore

        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_visible(True)        
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)       

        return fig

    def __repr__(self):
        return f"<{self.__class__.__name__}(name = {self.modelname})>"