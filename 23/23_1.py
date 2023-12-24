import logging
logging.basicConfig(level=logging.DEBUG)
import numpy as np
from dijkstra import dijkstra
from collections import defaultdict


class Maze:
    def __init__(self, grid):
        self.G = grid
        self.past = defaultdict(set)

    def __getitem__(self, u):
        i, j, past = u
        past = set(past)
        idim, jdim = self.G.shape
        vv = set()
        current = self.G[i, j]
        if current == "^" and 0 < i:
            vv.add((i-1, j))
        elif current == "v" and i < idim - 1:
            vv.add((i+1, j))
        elif current == "<" and 0 < j:
            vv.add((i, j-1))
        elif current == ">" and j < jdim - 1:
            vv.add((i, j+1))
        elif current == ".":
            if 0 < i:
                vv.add((i-1, j))
            if i < idim - 1:
                vv.add((i+1, j))
            if 0 < j:
                vv.add((i, j-1))
            if j < jdim - 1:
                vv.add((i, j+1))

        vv = vv.difference(past)
        nei = []
        for v in vv:
            if self.G[v] == "#":
                continue
            nei_past = past.copy()
            nei_past.add(v)
            nei_past = tuple(nei_past)
            nei_node = (v[0], v[1], nei_past)
            nei.append((nei_node, -1))

        return nei

    def is_goal(self, u):
        return u[0] == (self.G.shape[0]-1)


def read(filename):
    return np.array([ list(l.strip()) for l in open(filename) ])


def dump_grid(g):
    for row in g:
        print("".join(row))

def main(filename):
    grid = read(filename)
    print(grid)

    maze = Maze(grid)
    start = (0, 1, ((0, 1)))
    path, d = dijkstra(maze, start, lambda u: maze.is_goal(u), debug_freq=1)
    print(path)

    P = grid.copy()
    for i, j, _ in path:
        P[i, j] = "O"
    dump_grid(P)
    print(d)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
