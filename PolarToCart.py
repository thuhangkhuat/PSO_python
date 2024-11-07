import numpy as np

def polar_to_cart(sol, model):
    # Start location
    drone_radius = 5
    xs, ys = model['start']

    # Solution in Spherical space
    r = sol['r'].flatten()
    phi = sol['phi'].flatten()
    # Initialize lists for Cartesian coordinates
    x = [xs + r[0] * np.cos(phi[0])]
    y = [ys + r[0] * np.sin(phi[0])]

    # Check limits for the first coordinate
    x[0] = np.clip(x[0], model['xmin'] - drone_radius, model['xmax'] - drone_radius)
    y[0] = np.clip(y[0], model['ymin'] - drone_radius, model['ymax']- drone_radius)

    # Compute the next Cartesian coordinates
    for i in range(1, model['n']):
        x_i = x[i - 1] + r[i] * np.cos(phi[i])
        y_i = y[i - 1] + r[i] * np.sin(phi[i])

        # Apply boundary limits
        x.append(np.clip(x_i, model['xmin'], model['xmax']))
        y.append(np.clip(y_i, model['ymin'], model['ymax']))

    # Return the Cartesian coordinates as a dictionary
    position = {
        'x': x,
        'y': y,
    }
    return position
