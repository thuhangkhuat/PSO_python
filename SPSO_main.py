import numpy as np
import matplotlib.pyplot as plt
import math
import time
import pickle
# import sys
# import os
# sys.path.append(os.path.abspath('/home/hangktt/rrt_ws/SPSO_python'))
from MyCost import my_cost
from CreateModel import create_model
from CreateRandomSolution import create_random_solution
from PlotSulotion import plot_solution

# PSO parameters
MaxIt = 100
nPop = 500
w = 1
wdamp = 0.98
c1 = 0.5
c2 = 0.5
paths = []
# Initialization
model = create_model()
nVar = model['n']
VarSize = (1, nVar)
drone_radius = 5
# Variable limits
VarMin = {'x': model['xmin'], 'y': model['ymin']}
VarMax = {'x': model['xmax'], 'y': model['ymax']}
alpha = 0.01
VelMax = {'x': alpha*(VarMax['x'] - VarMin['x']), 'y': alpha*(VarMax['y'] - VarMin['y'])}
VelMin = {k: -v for k, v in VelMax.items()}

# Initialize particles
particles = []
GlobalBest = {'Cost': float('inf')}
st = time.time()
for k in range (len(model['end'])):
    for _ in range(nPop):
        particle = {
            'Position': create_random_solution(VarSize, VarMin, VarMax),
            'Velocity': {'x': np.zeros(VarSize), 'y': np.zeros(VarSize)},
        
            'Best': {'Position': None, 'Cost': float('inf')}
        }
        

        particle['Cost'] = my_cost(particle['Position'],model,k)
        particle['Best'] = {'Position': particle['Position'], 'Cost': particle['Cost']}
        if particle['Best']['Cost'] <= GlobalBest['Cost']:
            GlobalBest = particle['Best']
        particles.append(particle)
    BestCost = np.zeros(MaxIt)

    # PSO main loop
    for it in range(MaxIt):
        BestCost[it] = GlobalBest['Cost']
        for i in range(nPop):
            for var in ['x', 'y']:
                # Update velocity
                particles[i]['Velocity'][var] = (w * particles[i]['Velocity'][var]
                                                + c1 * np.random.rand(*VarSize) * (particles[i]['Best']['Position'][var] - particles[i]['Position'][var])
                                                + c2 * np.random.rand(*VarSize) * (GlobalBest['Position'][var] - particles[i]['Position'][var]))
                # Apply velocity bounds
                particles[i]['Velocity'][var] = np.clip(particles[i]['Velocity'][var], VelMin[var], VelMax[var])

                # Update position
                particles[i]['Position'][var] += particles[i]['Velocity'][var]
                particles[i]['Position'][var] = np.clip(particles[i]['Position'][var], VarMin[var], VarMax[var])

            # Evaluate cost
            particles[i]['Cost'] = my_cost(particles[i]['Position'],model,k)
            if particles[i]['Cost'] < particles[i]['Best']['Cost']:
                particles[i]['Best'] = {'Position': particles[i]['Position'], 'Cost': particles[i]['Cost']}
                if particles[i]['Best']['Cost'] < GlobalBest['Cost']:
                    GlobalBest = particles[i]['Best']
                    
        w *= wdamp
    BestPosition = GlobalBest['Position']
    if GlobalBest['Cost'] == float('inf'):
        success = 0
    else:
        success = 1
    path = np.column_stack((GlobalBest['Position']['x'].flatten(), GlobalBest['Position']['y'].flatten()))
    path = np.vstack(([model['start'][0], model['start'][1]], path))
    path = np.vstack((path,[model['end'][k,0], model['end'][k,1]]))
    paths.append(path)
    # plot_solution(BestPosition, model,k)
pt = time.time() - st
print(paths)
print(pt)
#Plot results
scenario = 4
counter = 0
if success:
        print("PSO done: {:.4f}s".format(pt))
        with open('data/scen{}_pso_{}.txt'.format(scenario, counter), 'wb') as f:
            d = dict()
            d["paths"] = paths
            d["pt"] = pt
            pickle.dump(d, f)
else:
    print("Failed.")

