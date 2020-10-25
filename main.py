##### EXAMPLE USAGE SCRIPT #######


import os
import numpy as np
import pkmodel as pk

t_0 = 0
t_end = 1
precison = 1000

model1_args = {
    'name': 'model1',
    'Q_p1': 3.0,
    'V_c': 2.0,
    'V_p1': 0.10,
    'CL': 2.0
}

model2_args = {
    'name': 'iv-2 comp',
    'V_c': 1.0,
    'CL': 1.0,
    'k_a': 5
}

# Protocol
trial_protocol = pk.Protocol(quantity = 2, t_start = t_0, t_end=t_end, n = precison)
X = trial_protocol.linear_dose()

# Model
trial1 = pk.Model(2,model1_args,'iv',X)
trial2 = pk.Model(2,model2_args,'sc',X)
models = [trial1,trial2]

# Solution
trial_sol = pk.Solution(models,
    t_eval = np.linspace(t_0, t_end, precison),y0=[[0,0],[0,0]])
trial_sol.analyse_models()

# Visualisation
labels = [model1_args['name'],model2_args['name']]

path = []
for model in models:
    path.append(os.path.join('data',model.model_args['name']))

trial_vis = pk.Visualisation(path, labels, [trial1.dose_type,trial2.dose_type])
trial_vis.visualise(labels,os.path.join('data/plots', 'testplot.png'))