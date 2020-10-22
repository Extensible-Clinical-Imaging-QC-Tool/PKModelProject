#
# Solution class
#
import numpy as np
import scipy.integrate
class Solution:
    """A Pharmokinetic (PK) model solution

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    """
   
    def __init__(self, list_of_models, t_eval, y0 = [0,0]):
        self.models = list_of_models
        self.y0 = np.array(y0)
        self.t_eval = t_eval
    
    def analyse_models(self):
        for model in self.models:
            args = self.get_arguments(model)
            sol = self._integrate(model)
            self._save_to_csv(sol)
        return sol
    
    def _get_arguments(self, model):
        return model.args #function/property of model from model class?
    
    def _integrate(self, model):
        sol = scipy.integrate.solve_ivp(fun =  lambda t, y: model.rhs(t, y, *args), #function for getting rhs?
         t_span = [self.t_eval[0], self.t_eval[-1]],
         y0 = self.y0, t_eval = self.t_eval
        )
        return sol
    
    def _save_to_csv(self, sol):
        # Alex's csv function







