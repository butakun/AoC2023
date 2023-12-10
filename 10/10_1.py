import numpy as np


def read(filename):
    grid = [list(l.strip()) for l in open(filename)]
    grid = np.array(grid)
    return grid


def guess_connection(grid, i, j):
    north_cell, south_cell, east_cell, west_cell = ".", ".", ".", "."
    if i > 0:
        north_cell = grid[i-1, j]
    if j > 0:
        west_cell = grid[i, j-1]
    if i < grid.shape[0] - 1:
        south_cell = grid[i+1, j]
    if j < grid.shape[1] - 1:
        east_cell = grid[i, j+1]

    north, south, east, west = False, False, False, False
    north = north_cell == "|" or north_cell == "7" or north_cell == "F"
    south = south_cell == "|" or south_cell == "L" or south_cell == "J"
    west = west_cell == "-" or west_cell == "L" or west_cell == "F"
    east = east_cell == "-" or east_cell == "J" or east_cell == "7"

    if north and south:
        return "|"
    elif west and east:
        return "-"
    elif north and east:
        return "L"
    elif north and west:
        return "J"
    elif south and west:
        return "7"
    elif south and east:
        return "F"


def build_network(grid, i, j):
    network = {}
    nodes = [(i, j)]
    while nodes:
        node = nodes.pop()
        if node in network:
            continue
        i, j = node
        print(node)
        if grid[node] == "|":
            neighbors = [(i-1, j), (i+1, j)]
        elif grid[node] == "-":
            neighbors = [(i, j-1), (i, j+1)]
        elif grid[node] == "L":
            neighbors = [(i-1, j), (i, j+1)]
        elif grid[node] == "J":
            neighbors = [(i-1, j), (i, j-1)]
        elif grid[node] == "7":
            neighbors = [(i, j-1), (i+1, j)]
        elif grid[node] == "F":
            neighbors = [(i, j+1), (i+1, j)]
        nodes.extend(neighbors)
        network[node] = neighbors

    return network


def get_loop(network, i, j):
    start = (i, j)
    loop = [start, network[start][0]]
    closed = False
    while not closed:
        node1 = loop[-2]
        node2 = loop[-1]
        for nei in network[node2]:
            if nei != node1:
                if nei == start:
                    closed = True
                    break
                loop.append(nei)
    return loop


def main(filename):
    grid = read(filename)
    print(grid)

    i, j = np.where(grid == 'S')
    start = i[0], j[0]

    start_cell = guess_connection(grid, *start)
    print(start_cell)

    grid[start] = start_cell
    print(grid)

    network = build_network(grid, *start)
    print(network)

    loop = get_loop(network, *start)
    print(loop)

    print(len(loop))
    farthest = len(loop) / 2
    print(int(farthest))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
