import numpy as np
import sys


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


def flood(grid, network, loop):
    s = grid.shape
    pond = np.zeros((s[0] * 2 + 1, s[1] * 2 + 1), dtype=grid.dtype)
    pond[:, :] = "."

    for node in loop:
        i, j = node
        I, J = i * 2 + 1, j * 2 + 1
        pipe = grid[node]
        pond[I, J] = "P"
        if pipe == "|" or pipe == "L" or pipe == "J":
            pond[I-1, J] = "P"
        if pipe == "|" or pipe == "7" or pipe == "F":
            pond[I+1, J] = "P"
        if pipe == "-" or pipe == "7" or pipe == "J":
            pond[I, J-1] = "P"
        if pipe == "-" or pipe == "L" or pipe == "F":
            pond[I, J+1] = "P"

    start1, start2 = None, None
    for node in loop:
        if grid[node] != "|":
            continue
        i, j = node
        I, J = i * 2 + 1, j * 2 + 1
        pond[I, J-1] = "-"
        pond[I, J+1] = "+"
        start1 = I, J-1
        start2 = I, J+1
        break
    assert (start1 is not None) and (start2 is not None)

    # (i, j) is pond-coord below
    outside_marker = None
    IDIM, JDIM = pond.shape
    for start in [start1, start2]:
        nodes = [start]
        marker = pond[start]
        while nodes:
            node = nodes.pop()
            i, j = node
            imin, imax = max(0, i-1), min(IDIM-1, i+1)
            jmin, jmax = max(0, j-1), min(JDIM-1, j+1)
            for ii in range(imin, imax+1):
                for jj in range(jmin, jmax+1):
                    p = pond[ii, jj]
                    if p != "P" and p != marker:
                        pond[ii, jj] = marker
                        nodes.append((ii, jj))
                        if ii == 0 or jj == 0 or ii == IDIM-1 or jj == JDIM-1:
                            outside_marker = marker

    inside_marker = "-" if outside_marker == "+" else "+"
    return pond, inside_marker, outside_marker


def condensed_print(g, file=sys.stdout):
    for i in range(g.shape[0]):
        line = "".join(g[i, :])
        print(line, file=file)


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

    big_pond, inside, outside = flood(grid, network, loop)
    #condensed_print(big_pond)

    small_pond = big_pond[1::2, 1::2]
    condensed_print(small_pond)
    print(f"inside = {inside}, outside = {outside}")

    area = np.sum(small_pond == inside)
    print(area)

    with open("small_pond.txt", "w") as f:
        condensed_print(small_pond, f)
    with open("big_pond.txt", "w") as f:
        condensed_print(big_pond, f)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
