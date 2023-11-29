import numpy as np

thickness = np.array([4, 5, 5, 5, 5, 9, 17, 17, np.Inf])
velocities = np.array([5.3, 5.6, 6.2, 6.9, 7.4, 7.7, 7.9, 8.1, 8.3 ])
depths = np.cumsum(thickness)

sind = lambda degrees: np.sin(np.deg2rad(degrees))
asind = lambda x: np.ras2deg(np.arcsin(v))
get_velocity = lambda depth: velocities[np.where(depths >= depth)[0][0]]
ray_parameter = lambda depth, theta: np.sin(theta)/velocity

def estimate_thetas(p, depth):
    Vup = velocities[np.where(depths < depth)[0]]
    thetas = asind(p*Vup)
    return thetas


