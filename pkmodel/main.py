import numpy as np
import os


from solution import Solution
from model import Model
from visualisation import Visualisation
from Dose import Protocol

t_0 = 0
t_end = 1
precison = 1000

model1_args = {
    'name': 'model1',
    'Q_p1': 1.0,
    'V_c': 1.0,
    'V_p1': 1.0,
    'CL': 2.0,
#    'k_a': 3.0

}

model2_args = {
    'name': 'model2',
    'Q_p1': 1.0,
    'V_c': 1.0,
    'V_p1': 1.0,
    'Q_p2': 0.5,
    'V_p2': 0.25,
    'CL': 2.0,
    'k_a':3.0
    }

print('trial')
# Protocol
trial_protocol = Protocol(quantity = 6, t_start = t_0, t_end=t_end, n = precison)
X = trial_protocol.instantaneous_dose(T1 = 10)

# Model
trial = Model(3,model2_args,'sc',X)

# Solution
trial_sol = Solution([trial],
    t_eval = np.linspace(t_0, t_end, precison))
trial_sol.analyse_models()

# Visualisation
trial_vis = Visualisation([os.path.join(os.getcwd(), 
trial.model_args['name'])], ['3'])
trial_vis.visualise(['3'])