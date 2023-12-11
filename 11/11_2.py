import numpy as np
import sys
import itertools


def read(filename):
    grid = [list(l.strip()) for l in open(filename)]
    grid = np.array(grid)
    return grid


def gaps(grid):
    rows = []
    for i in range(grid.shape[0]):
        if np.all(grid[i, :] == "."):
            rows.append(i)

    cols = []
    for j in range(grid.shape[1]):
        if np.all(grid[:, j] == "."):
            cols.append(j)

    return np.array(rows), np.array(cols)


def distance(g1, g2, rows, cols, n_gaps):
    imin = min(g1[0], g2[0])
    imax = max(g1[0], g2[0])
    rows_ = np.logical_and(imin <= rows, rows <= imax)

    jmin = min(g1[1], g2[1])
    jmax = max(g1[1], g2[1])
    cols_ = np.logical_and(jmin <= cols, cols <= jmax)

    d = abs(int(g2[0] - g1[0])) + abs(int(g2[1] - g1[1]))
    d += sum(rows_) * (n_gaps - 1)
    d += sum(cols_) * (n_gaps - 1)

    return d

def condensed_print(g, file=sys.stdout):
    for i in range(g.shape[0]):
        line = "".join(g[i, :])
        print(line, file=file)


def main(filename):
    grid = read(filename)
    condensed_print(grid)

    rows, cols = gaps(grid)
    print(rows, cols)

    ii, jj = np.where(grid == "#")
    galaxies = [ (i, j) for i, j in zip(ii, jj) ]

    sum = 0
    for g1, g2 in itertools.combinations(galaxies, 2):
        d = distance(g1, g2, rows, cols, n_gaps=1000000)
        print(f"{g1} - {g2} = {d}")
        sum += d
    print(sum)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
