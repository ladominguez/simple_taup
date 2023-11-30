from utils import *

if __name__ == "__main__":
    depth = 12
    station_distance =17
    for theta in np.linspace(0, 70, 10):
        xi, distances = estimate_distances(theta, depth)
        print('theta = %5.3f xi = %5.3f '% (theta, xi))


    #theta = solve_theta(station_distance, depth)
    #print('theta = ', theta)
    #xi, distances = estimate_distances(theta, depth)
    #print('xi = ', xi)
    #print('distances = ', distances)    
    fig = plot_model(max_dist=station_distance + 10)
    fig = plot_solution(fig, depth, station_distance)
    fig.savefig('model.png')

