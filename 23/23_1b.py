import logging
logging.basicConfig(level=logging.DEBUG)
import numpy as np
from dijkstra import dijkstra
from collections import defaultdict

logger = logging.getLogger(__name__)


class GridMaze:
    def __init__(self, grid):
        self.G = grid

    def __getitem__(self, u):
        i, j = u
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
        return [ (v, -1) for v in vv if self.G[v] != "#" ]

    def is_goal(self, u):
        return u[0] == (self.G.shape[0]-1)


class Maze:
    def __init__(self, G, grid_nrows):
        self.G = G
        self.goal_row = grid_nrows - 1

    def __getitem__(self, u_with_past):
        u, past = u_with_past
        past = set(past)
        vvw = self.G[u]
        vv = set([v for v, w in vvw])
        vv = vv.difference(past)
        nei_nodes = []
        for v, w in vvw:
            if v not in vv:
                continue
            nei_past = past.copy()
            nei_past.add(v)
            nei_past = tuple(nei_past)
            nei_node = ((v, nei_past), w)
            nei_nodes.append(nei_node)
        return nei_nodes

    def is_goal(self, u_with_past):
        u, past = u_with_past
        return u[0] == self.goal_row


def read(filename):
    return np.array([ list(l.strip()) for l in open(filename) ])


def dump_grid(g):
    for row in g:
        print("".join(row))


def simplify_maze(maze):
    # extract all the chars that are not "#"
    ii, jj = np.where(maze.G != "#")
    nodes = [ (i, j) for i, j in zip(ii, jj) ]

    G = defaultdict(set)
    E = dict()

    edge_key = lambda node1, node2: (node1, node2) if node1 < node2 else (node2, node1)

    for u in nodes:
        neighbors = maze[u]
        for v, weight in neighbors:
            G[u].add(v)
            edge = edge_key(u, v)
            E[edge] = weight

    for u, vv in G.items():
        logger.debug(f"{u}: {vv}")
    logger.debug(f"# nodes = {len(nodes)}")

    visited = set()
    remaining = [(0, 1)]
    while remaining:
        print(f"{remaining=}")
        u = remaining.pop(0)
        if u in visited:  # visited can have duplicate nodes
            continue
        visited.add(u)

        vv = list(G[u])
        degrees = len(vv)
        if degrees == 1:
            v = vv[0]
            if v not in visited:
                remaining.append(v)
        elif degrees == 2:
            # remove node u, connecting v1 and v2
            v1 = vv[0]
            v2 = vv[1]
            logger.debug(f"contracting {v1} - {u} - {v2}")
            logger.debug(f"  {G[v1]=}")
            logger.debug(f"  {G[v2]=}")
            w1 = E[edge_key(u, v1)]
            w2 = E[edge_key(u, v2)]
            G.pop(u)
            logger.debug(f"  removed {u}")
            if u in G[v1]:
                G[v1].remove(u)
            if u in G[v2]:
                G[v2].remove(u)
            G[v1].add(v2)
            G[v2].add(v1)
            E[edge_key(v1, v2)] = w1 + w2
            if v1 not in visited:
                remaining.append(v1)
            if v2 not in visited:
                remaining.append(v2)
        elif degrees > 2:
            for v in vv:
                if v not in visited:
                    remaining.append(v)
        else:
            raise ValueError(f"{u=}, {vv=}")
    logger.debug(f"# nodes after edge contraction = {len(G.keys())}")

    simplified = defaultdict(set)
    for u, vv in G.items():
        vw = []
        for v in vv:
            edge = edge_key(u, v)
            weight = E[edge]
            vw.append((v, weight))
        simplified[u] = set(vw)
        logger.debug(f"{u}: {vw}")

    return simplified


def main(filename):
    grid = read(filename)
    grid_maze = GridMaze(grid)
    simplified = simplify_maze(grid_maze)

    maze = Maze(simplified, grid.shape[0])
    print(f"{maze.goal_row=}")

    start = ((0, 1), ((0, 1)))
    path, d = dijkstra(maze, start, lambda u: maze.is_goal(u), debug_freq=1)
    print(path)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
