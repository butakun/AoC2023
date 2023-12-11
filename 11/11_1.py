import numpy as np
import sys
import itertools


def read(filename):
    grid = [list(l.strip()) for l in open(filename)]
    grid = np.array(grid)
    return grid


def expand(grid):
    rows = []
    for i in range(grid.shape[0]):
        if np.all(grid[i, :] == "."):
            rows.append(i)
    print(rows)

    cols = []
    for j in range(grid.shape[1]):
        if np.all(grid[:, j] == "."):
            cols.append(j)
    print(cols)

    grid = np.insert(grid, rows, ".", axis=0)
    print("rows inserted")
    condensed_print(grid)

    grid = np.insert(grid, cols, ".", axis=1)
    print("cols inserted")
    condensed_print(grid)

    return grid


def condensed_print(g, file=sys.stdout):
    for i in range(g.shape[0]):
        line = "".join(g[i, :])
        print(line, file=file)


def main(filename):
    grid = read(filename)
    condensed_print(grid)

    grid = expand(grid)

    ii, jj = np.where(grid == "#")
    galaxies = [ (i, j) for i, j in zip(ii, jj) ]
    print(galaxies)
    
    sum = 0
    for g1, g2 in itertools.combinations(galaxies, 2):
        d = abs(int(g2[0] - g1[0])) + abs(int(g2[1] - g1[1]))
        print(f"{g1} - {g2} = {d}")
        sum += d
    print(sum)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
