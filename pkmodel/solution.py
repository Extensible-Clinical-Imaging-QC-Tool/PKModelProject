#
# Solution class
#
import numpy as np
import scipy.integrate
import csv as csv
import os
class Solution:
    """A Pharmokinetic (PK) model solution

    Parameters
    ----------

    :param list_of_models: list of Model class instances, required
        
    :param t_eval: array_like, required
        Time steps at which the solution should be computed.
    
    :param y0: a list of list objects, required
        Initial amount of drug in all compartments for each model. 
        Should be a list of each model's initial conditions.

        e.g. [[0,0], [1,1]]

    """
   

    def __init__(self, list_of_models, t_eval, y0):

        self.models = list_of_models
        self.y0 = y0
        self.t_eval = t_eval

    
    def analyse_models(self):
        """
        Computes a solution of each model specified in the list of models.
        The solution data for each model is saved as a csv in the provided path.

        Returns
        -------

        :return sol_list: a list of solution Bunch objects with defined fields.
            Time points are defined as 't' and values of solution are defined as 'y'.

        """
        count = 0
        sol_list = []
        for model in self.models:
            # Get arguments of the model using Model's make_arg methods
            args = model.make_args()
            # Create a 1D array of initial conditions for the evaluated model
            y0 = np.array(self.y0[count])
            sol = self._integrate(model,args,y0)
            sol_list.append(sol)
            count += 1
            path = os.path.join(os.getcwd(),model.model_args['name'])
            self._save_to_csv(sol.t,sol.y,path)
        return sol_list
    
    
    def _integrate(self, model,args, y0):
        """
        Numerically integrates a provided PK model using scipy's solve_ivp

        Parameters
        ----------

        model: Model class instance, required.
            A Pharmokinetic model.
        
        args: list, required.
            A list of parameters of the Pharmokinetic model.
        
        Returns
        -------

        sol: Bunch object with defined time points and values of solution.
            Refer to scipy's solve_ivp documentation

        """

        sol = scipy.integrate.solve_ivp(fun =  lambda t, y: model.rhs(t, y, args),
         t_span = [self.t_eval[0], self.t_eval[-1]],
         y0 = y0, t_eval = self.t_eval)
         
        return sol
    
    def _save_to_csv(self,time, sol, save_file_path):
        """
        Saves the provided time steps and solution to a .csv file.

        Parameters
        ----------
        time: list or array of floats, required
            A list or array of time step values.

        sol: list or array of floats, required
            A list or array of solution values. Must be the
            same length as the time parameter.

        save_file_path: str or PathLike or file-like object, required
            If str or PathLike or file-like object, then it will be used 
            as the file path or file name of the saved figure.

            e.g. '../path/to/solution_data.csv'

        """
        if len(time) != len(sol[1]):
            raise ValueError('The solution must be the same length as the time.')

        solution_data = np.hstack( (time.reshape((len(time),1)), sol.transpose()) )
        with open(save_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(solution_data)







