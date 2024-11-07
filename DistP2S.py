import numpy as np

def dist_p2s(x, a, b):
    d_ab = np.linalg.norm(np.array(a) - np.array(b))
    d_ax = np.linalg.norm(np.array(a) - np.array(x))
    d_bx = np.linalg.norm(np.array(b) - np.array(x))
    
    if d_ab != 0:
        if np.dot(np.array(a) - np.array(b), np.array(x) - np.array(b)) * np.dot(np.array(b) - np.array(a), np.array(x) - np.array(a)) >= 0:
            # Calculate distance from point to line segment
            A = np.vstack((np.array(b) - np.array(a), np.array(x) - np.array(a)))
            dist = abs(np.linalg.det(A)) / d_ab
        else:
            dist = min(d_ax, d_bx)
    else:
        dist = d_ax  # If a and b are identical
    
    return dist
