import logging
logging.basicConfig(level=logging.INFO)
import numpy as np


def read(filename):
    grid = np.array([ list(l.strip()) for l in open(filename) ])
    return grid


def tilt(grid, direction):
    idim, jdim = grid.shape
    if direction == "N":
        irange = range(idim)
    elif direction == "S":
        irange = reversed(range(idim))
    elif direction == "W":
        irange = range(idim)
    elif direction == "E":
        irange = range(idim)
    for i in irange:
        if direction == "N":
            jrange = range(jdim)
        elif direction == "S":
            jrange = range(jdim)
        elif direction == "W":
            jrange = range(jdim)
        elif direction == "E":
            jrange = reversed(range(jdim))
        for j in jrange:
            if grid[i, j] != "O":
                continue
            i0, j0 = None, None
            if direction == "N":
                j0 = j
                for k in reversed(range(0, i)):
                    if grid[k, j] != ".":
                        break
                    i0 = k
            elif direction == "W":
                i0 = i
                for k in reversed(range(0, j)):
                    if grid[i, k] != ".":
                        break
                    j0 = k
            elif direction == "S":
                j0 = j
                for k in range(i+1, idim):
                    if grid[k, j] != ".":
                        break
                    i0 = k
            elif direction == "E":
                i0 = i
                for k in range(j+1, jdim):
                    if grid[i, k] != ".":
                        break
                    j0 = k
            if i0 is not None and j0 is not None:
                logging.debug(f"{i}, {j} -> {i0}, {j0}")
                grid[i0, j0] = "O"
                grid[i, j] = "."


def main(filename):
    grid = read(filename)
    print(grid)

    idim, jdim = grid.shape

    for cycle in range(1000):
        tilt(grid, "N")
        tilt(grid, "W")
        tilt(grid, "S")
        tilt(grid, "E")

        weight = 0
        ii, jj = np.where(grid == "O")
        for i, j in zip(ii, jj):
            w = idim - i
            weight += w
        logging.info(f"{cycle} {weight}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
