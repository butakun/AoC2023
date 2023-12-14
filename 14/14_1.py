import numpy as np
import sys
import itertools


def read(filename):
    grid = np.array([ list(l.strip()) for l in open(filename) ])
    return grid


def main(filename):
    grid = read(filename)
    print(grid)

    idim, jdim = grid.shape
    for i in range(idim):
        for j in range(jdim):
            if grid[i, j] != "O":
                continue
            i0 = None
            for k in reversed(range(0, i)):
                if grid[k, j] != ".":
                    break
                i0 = k
            if i0 is not None:
                print(i, j, "->", i0, j)
                grid[i0, j] = "O"
                grid[i, j] = "."

    print(grid)

    weight = 0
    ii, jj = np.where(grid == "O")
    for i, j in zip(ii, jj):
        w = idim - i
        print(i, j, grid[i, j], w)
        weight += w
    print(weight)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
