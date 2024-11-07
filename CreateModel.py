import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image

def create_model():
    # Load elevation data
    MAPSIZE_X = 1000 # Dimensions of the map
    MAPSIZE_Y = 800


    # Threat parameters as cylinders
    obs_circle = np.array([[640,  80, 40],
              [800, 400, 40],
              [120, 440, 40],
              # [240, 720, 40],
              # [450, 470, 80],
              [690, 670, 80],
              [320, 120, 80],
              # [780, 135, 60],
              # [120, 245, 60],
              # [132, 632, 60],
              # [640, 290, 60],
              [440, 650, 60],
              [870, 550, 60],
              # [640, 470, 40],
              # [455, 250, 40],
              [260, 540, 60],
              # [290, 320, 40],
              # [900, 710, 40],
              # [120, 85, 40],
              [880, 270, 80],
              [490, 110, 60]])

    # Map boundaries
    xmin, xmax = 0, MAPSIZE_X-1
    ymin, ymax = 0, MAPSIZE_Y-1
    # Start and end positions
    start_location = np.array([920, 80])
    end_location = np.array([[70, 750],[50,  40],[790, 760]])

    # Number of path nodes (excluding the start node)
    n = 10

    # Model as a dictionary
    model = {
        "start": start_location,
        "end": end_location,
        "n": n,
        "xmin": xmin,
        "xmax": xmax,
        "ymin": ymin,
        "ymax": ymax,
        "MAPSIZE_X": MAPSIZE_X,
        "MAPSIZE_Y": MAPSIZE_Y,
        "obs_circle": obs_circle
    }

    # plot_model(model)
    return model


