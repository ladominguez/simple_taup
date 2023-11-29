from utils import *

if __name__ == "__main__":
    depth = 12
    takeoff = 32

    p = ray_parameter(depth, takeoff)
    thetas = estimate_thetas(p, depth)
