import numpy as np
import matplotlib.pyplot as plt
import math
# import sys
# import os
# sys.path.append(os.path.abspath('/home/hangktt/rrt_ws/SPSO_python'))
from MyCost import my_cost
from CreateModel import create_model
from CreateRandomSolution import create_random_solution
from PolarToCart import polar_to_cart
from PlotSulotion import plot_solution

# PSO parameters
MaxIt = 100
nPop = 500
w = 1
wdamp = 0.98
c1 = 1.5
c2 = 1.5

# Initialization
model = create_model()
CostFunction = lambda x: my_cost(x, model)
nVar = model['n']
VarSize = (1, nVar)

# Variable limits
VarMin = {'r': -50, 'phi': -math.pi}
VarMax = {'r': 50, 'phi': math.pi}
alpha = 0.5
VelMax = {'r':alpha*(VarMax['r']-VarMin['r']),'phi':alpha*(VarMax['phi']-VarMin['phi'])}
VelMin = {k: -v for k, v in VelMax.items()}

# Initialize particles
particles = []
GlobalBest = {'Cost': float('inf')}

for _ in range(nPop):
    particle = {
        'Position': create_random_solution(VarSize, VarMin, VarMax),
        'Velocity': {'r': np.zeros(VarSize), 'phi': np.zeros(VarSize)},
       
        'Best': {'Position': None, 'Cost': float('inf')}
    }
    

    particle['Cost'] = CostFunction(polar_to_cart(particle['Position'],model))
    particle['Best'] = {'Position': particle['Position'], 'Cost': particle['Cost']}
    if particle['Best']['Cost'] <= GlobalBest['Cost']:
        GlobalBest = particle['Best']
    particles.append(particle)
BestCost = np.zeros(MaxIt)

# PSO main loop
for it in range(MaxIt):
    BestCost[it] = GlobalBest['Cost']
    for i in range(nPop):
        for var in ['r', 'phi']:
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
        particles[i]['Cost'] = CostFunction(polar_to_cart(particle['Position'],model))
        if particles[i]['Cost'] < particles[i]['Best']['Cost']:
            particles[i]['Best'] = {'Position': particles[i]['Position'], 'Cost': particles[i]['Cost']}
            if particles[i]['Best']['Cost'] < GlobalBest['Cost']:
                GlobalBest = particles[i]['Best']
                
    w *= wdamp
    print(f"Iteration {it + 1}: Best Cost = {BestCost[it]}")

# Plot results
BestPosition = polar_to_cart(GlobalBest['Position'],model)
print("Best solution...",BestPosition)
plot_solution(BestPosition, model)
plt.figure()
plt.plot(BestCost, linewidth=2)
plt.xlabel('Iteration')
plt.ylabel('Best Cost')
plt.grid()
plt.show()
