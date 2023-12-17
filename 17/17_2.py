import logging
logging.basicConfig(level=logging.DEBUG)
import numpy as np
from dijkstra import dijkstra, a_star
from visual import SearchVisualLogger


def read(filename):
    return np.array([ [int(c) for c in l.strip()] for l in open(filename) ])


class World:
    def __init__(self, grid):
        self.grid = grid

    def __getitem__(self, u):
        i, j, direction, steps = u
        # currently at (i, j), has moved "steps" steps in "direction"

        idim, jdim = self.grid.shape

        vv = []
        if direction == "N":
            if i > 0 and steps < 10:
                vv.append((i-1, j, "N", steps+1))
            if steps >= 4:
                if j > 0:
                    vv.append((i, j-1, "W", 1))
                if j < jdim - 1:
                    vv.append((i, j+1, "E", 1))
        elif direction == "S":
            if i < idim - 1 and steps < 10:
                vv.append((i+1, j, "S", steps+1))
            if steps >= 4:
                if j > 0:
                    vv.append((i, j-1, "W", 1))
                if j < jdim - 1:
                    vv.append((i, j+1, "E", 1))
        elif direction == "W":
            if j > 0 and steps < 10:
                vv.append((i, j-1, "W", steps+1))
            if steps >= 4:
                if i > 0:
                    vv.append((i-1, j, "N", 1))
                if i < idim - 1:
                    vv.append((i+1, j, "S", 1))
        elif direction == "E":
            if j < jdim - 1 and steps < 10:
                vv.append((i, j+1, "E", steps+1))
            if steps >= 4:
                if i > 0:
                    vv.append((i-1, j, "N", 1))
                if i < idim - 1:
                    vv.append((i+1, j, "S", 1))
        elif direction is None:  # initial state
            assert i == 0 and j == 0
            vv.append((i+1, j, "S", 1))
            vv.append((i, j+1, "E", 1))
        else:
            raise ValueError(direction)

        nei = [ (v, self.grid[v[0], v[1]]) for v in vv ]
        return nei

    def HFunc(self, u):
        idim, jdim = self.grid.shape
        i, j = u[0], u[1]
        wi = idim - i - 1
        wj = jdim - j - 1
        return wi + wj

    def is_goal(self, u):
        idim, jdim = self.grid.shape
        return u[3] >= 4 and u[0] == idim - 1 and u[1] == jdim - 1


def main(filename, method, visualize):
    grid = read(filename)
    print(grid)

    idim, jdim = grid.shape
    print("idim, jdim =", idim, jdim)

    G = World(grid)
    start = (0, 0, None, 0)

    if visualize:
        vis_logger = SearchVisualLogger(open("vis.log", "w"))
        vis_logger.dimensions(idim, jdim)
    else:
        vis_logger = None

    if method == "dijkstra":
        path, d = dijkstra(G, start, lambda u: G.is_goal(u), debug_freq=1, vis_logger=vis_logger)
    elif method == "astar":
        path, d = dijkstra(G, start, lambda u: G.is_goal(u), debug_freq=1, vis_logger=None)
    print(path)
    print(d)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    parser.add_argument("--method", default="dijkstra")
    parser.add_argument("--vis", action="store_true")
    args = parser.parse_args()
    main(args.input, args.method, args.vis)
