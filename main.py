from utils import *

if __name__ == "__main__":
    depth = 12
    station_distance =17

    fig, axs = plot_model(max_dist=station_distance + 10)
    fig = plot_solution(fig, depth, station_distance)
    fig.savefig('model.png')

