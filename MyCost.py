import numpy as np
from DistP2S import dist_p2s
def my_cost(sol, model,i):
    J_inf = float('inf')
    n = model['n']
    
    # Input solution
    x = sol['x'].flatten()
    y = sol['y'].flatten()
    # x = sol['x']
    # y = sol['y']
    
    # Start and Final locations
    xs, ys= model['start']
    xf, yf= model['end'][i]
    
    # Concatenate all x, y, points
    x_all = np.array([xs, *x, xf])
    y_all = np.array([ys, *y, yf])

    N = len(x_all)  # Full path length

    #============================================
    # J1 - Cost for path length
    J1 = sum(np.linalg.norm([x_all[i+1] - x_all[i], y_all[i+1] - y_all[i]]) for i in range(N-1))

    #==============================================
    # J2 - threats/obstacles Cost
    threats = model['obs_circle']
    drone_size = 1
    danger_dist = 10 * drone_size
    J2 = 0
    for threat in threats:
        threat_x, threat_y, threat_radius = threat
        for j in range(N - 1):
            dist = dist_p2s([threat_x, threat_y], [x_all[j], y_all[j]], [x_all[j + 1], y_all[j + 1]])
            if dist > (threat_radius + drone_size):
                threat_cost = 0
            else:
                threat_cost = J_inf
            J2 += threat_cost
    
    # Weight coefficients
    b1, b2 = 1, 1

    # Overall cost
    cost = b1 * J1 + b2 * J2 
    return cost
