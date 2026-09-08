import torch 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np

from tirex import ForecastModel, load_model

from ..dataloading import load_data, process_data, EpiConfig

class TiRexModel:
    
    def __init__(self,
                 epiconfig: EpiConfig):
        
        self.modelcolor = "#1b9e77"
        self.modelname  = 'tirex'
        self.contextcolor = '#4a90d9' 
        self.testcolor  = '#d94e4e'          

        self.model: ForecastModel = load_model("NX-AI/TiRex", backend="torch") #type: ignore

        self.epicfg = epiconfig

        self.context_data, self.test_data = self._prepare_data()

    def _prepare_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        df_raw = load_data(self.epicfg)
        df_pcd = process_data(df_raw, self.epicfg)         

        ctx = df_pcd[df_pcd['context']].reset_index(drop=True)
        tst = df_pcd[df_pcd['test']].reset_index(drop=True)
        return ctx, tst

    def plot_split(self):
        title = f'{self.epicfg.disease.capitalize()} - weekly cases in Germany'

        fig, ax = plt.subplots(1,1,figsize = (10,4))
        sns.lineplot(self.context_data, x = 'timestamp', y = 'cases',  color = self.contextcolor, label = 'context', ax = ax)
        sns.lineplot(self.test_data,    x = 'timestamp', y = 'cases',  color = self.testcolor,    label = 'test', ax = ax)


        ax.legend(loc = 'upper left')
        ax.set_title(title, loc = 'left', fontweight = 'bold')
        ax.set_xlabel("")
        ax.set_ylabel("Cases")

        ymax = max(self.test_data['cases'].max(), self.context_data['cases'].max())

        ax.set_ylim([-0.01 * ymax, 1.01 * ymax])

        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_visible(True)        
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)             
        return fig

    def plot_preds(self, context : bool):
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


        ax.set_ylim([-0.01 * ymax, 1.01 * ymax])

        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_visible(True)        
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)       

        return fig


    def forecast(self):
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