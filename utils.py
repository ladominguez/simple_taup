import numpy as np
from matplotlib import pyplot as plt

thickness, velocities = np.loadtxt('model.txt', unpack=True, skiprows=1)
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
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(8,10))
    
    ax1.set_title('Model')
    ax1.set_xlabel('Distance [km]')
    ax1.set_ylabel('Depth [km]')
    ax1.set_xlim([0, max_dist])
    ax1.set_ylim([0, np.sum(thickness[thickness != np.Inf])+ 5])
    ax1.invert_yaxis()
    # add another subplot to the right

    for depth in depths:
        ax1.axhline(depth, color='red')
    # get y limits of ax1
    ylim = ax1.get_ylim()    
    ax2.step(np.append(velocities,velocities[-1]), 
            np.append(np.append(0,np.delete(depths, -1)),ylim[0]), color='green')
    ax2.invert_yaxis()
    ax2.set_title('P- wave velocity')
    ax2.set_xlabel('Velocity [km/s]')
    ax2.set_ylabel('Depth [km]')
    ax2.set_ylim(ylim)
    # add grid with dashed lines
    ax2.grid(linestyle='--')

    return fig, (ax1, ax2)

def plot_solution(fig, depth, station_distance):
    print("depths: ", depths)
    ax = fig.axes[0]
    theta = solve_theta(station_distance, depth)
    _, distances = estimate_distances(theta, depth)
    xi = np.append(0,distances)
    zi = np.append(np.flip(np.cumsum(get_depths(depth))),0)
    ax.plot(xi, zi, color='blue')
    ax.scatter(station_distance, 0, color='blue')
    return fig