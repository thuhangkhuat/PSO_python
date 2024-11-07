import numpy as np

def create_random_solution(var_size, var_min, var_max):
    # Random path nodes
    sol = {
        'x': np.random.uniform(var_min['x'], var_max['x'], var_size),
        'y': np.random.uniform(var_min['y'], var_max['y'], var_size)
    }
    # sol = {
    #     'r': np.random.uniform(var_min['r'], var_max['r'], var_size),
    #     'phi': np.random.uniform(var_min['phi'], var_max['phi'], var_size)
    # }
    return sol
