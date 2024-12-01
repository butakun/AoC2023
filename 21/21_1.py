import logging
logging.basicConfig(level=logging.INFO)
import numpy as np


def read(filename):
    return np.array([ list(l.strip()) for l in open(filename) ])


def condensed_print(g):
    for row in g:
        print("".join(row))


def main(filename):
    grid = read(filename)
    print(grid)

    idim, jdim = grid.shape

    i, j = np.where(grid == "S")
    grid[i, j] = "."
    i, j = i[0], j[0]
    front = [(i, j)]
    nsteps = 64
    for istep in range(nsteps):
        next_front = []
        while front:
            i0, j0 = front.pop(0)
            for di, dj in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                ii, jj = i0 + di, j0 + dj
                if ii >= 0 and ii < idim and jj >= 0 and jj < jdim:
                    if grid[ii, jj] == "." and (ii, jj) not in next_front:
                        next_front.append((ii, jj))
        front = next_front
        print(f"{istep}")

    grid_ = grid.copy()
    for i, j in front:
        grid_[i, j] = "O"
    condensed_print(grid_)

    print(front)
    print(len(front))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
