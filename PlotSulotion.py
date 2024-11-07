import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import CubicSpline
def plot_solution(sol, model,i):
    # Plot 3D view
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(model['xmin'], model['xmax'])
    ax.set_ylim(model['ymin'], model['ymax'])
    ax.set_title("2D Map with Threat Areas")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    for obs_circle in model['obs_circle']:
        x, y, radius = obs_circle
        circle = plt.Circle((x, y), radius, color='red', alpha=0.5)
        ax.add_patch(circle)

    plt.grid(True)

    x = sol['x'].flatten()
    y = sol['y'].flatten()
    # x = sol['x']
    # y = sol['y']
    
    
    # Start location
    xs = model['start'][0]
    ys = model['start'][1]
    
    # Final location
    xf, yf = model['end'][i]
    
    x_all = np.array([xs, *x, xf])
    y_all = np.array([ys, *y, yf])
    N = len(x_all)  # Real path length
    ax.plot(np.array(x_all), np.array(y_all), "blue",marker='o', linewidth=2)
    plt.plot(xs, ys, "bs", linewidth=5)
    plt.plot(xf, yf, "rs", linewidth=5)
    
    plt.show()




