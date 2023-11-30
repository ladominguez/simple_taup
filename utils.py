import numpy as np
from matplotlib import pyplot as plt

thickness = np.array([4, 5, 5, 5, 5, 9, 17, 17, np.Inf])
velocities = np.array([5.3, 5.6, 6.2, 6.9, 7.4, 7.7, 7.9, 8.1, 8.3 ])
depths = np.cumsum(thickness)

sind = lambda degrees: np.sin(np.deg2rad(degrees))
tand = lambda degrees: np.tan(np.deg2rad(degrees))
asind = lambda x: np.rad2deg(np.arcsin(x))
get_velocity = lambda depth: velocities[np.where(depths >= depth)[0][0]]
ray_parameter = lambda depth, theta: sind(theta)/get_velocity(depth)
get_depths = lambda depth: np.append(thickness[np.where(depths < depth)[0]],depth - depths[np.where(depths < depth)][-1])

def estimate_thetas(depth, takeoff):
    p = ray_parameter(depth, takeoff)
    Vup = velocities[np.where(depths < depth)[0]]
    thetas = asind(p*Vup)
    thetas = np.append(takeoff, thetas)
    return thetas

def estimate_distances(takeoff, depth):
    thetas = estimate_thetas(depth, takeoff)
    xi =  get_depths(depth)*tand(thetas)
    xi = np.cumsum(xi)
    return xi[-1], xi

def solve_theta(station_distance, depth):
    thetas = np.linspace(0,70, 201)
    distances = np.array([estimate_distances(takeoff_i, depth)[0] for takeoff_i in thetas])
    return thetas[np.argmin(np.abs(distances - station_distance))]

def plot_model(max_dist = 100):
    fig = plt.figure(figsize=(4,10))
    ax = fig.add_subplot(111)
    ax.set_title('Model')
    ax.set_xlabel('Distance [m]')
    ax.set_ylabel('Depth [m]')
    ax.set_xlim([0, max_dist])
    ax.set_ylim([0, np.sum(thickness[thickness != np.Inf])+ 5])
    ax.invert_yaxis()
    for depth in depths:
        ax.axhline(depth, color='red')
    return fig

def plot_solution(fig, depth, station_distance):
    ax = fig.axes[0]
    theta = solve_theta(station_distance, depth)
    _, distances = estimate_distances(theta, depth)
    xi = np.append(0,distances)
    zi = np.append(np.flip(np.cumsum(get_depths(depth))),0)
    ax.plot(xi, zi, color='blue')
    ax.scatter(station_distance, 0, color='blue')
    return fig