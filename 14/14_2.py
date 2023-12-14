import logging
logging.basicConfig(level=logging.INFO)
import numpy as np


def read(filename):
    grid = np.array([ list(l.strip()) for l in open(filename) ])
    return grid


def tilt(grid, direction):
    idim, jdim = grid.shape
    if direction == "N":
        irange = lambda : range(idim)
        jrange = lambda : range(jdim)
    elif direction == "S":
        irange = lambda : reversed(range(idim))
        jrange = lambda : range(jdim)
    elif direction == "W":
        irange = lambda : range(idim)
        jrange = lambda : range(jdim)
    elif direction == "E":
        irange = lambda : range(idim)
        jrange = lambda : reversed(range(jdim))
    for i in irange():
        for j in jrange():
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

    patterns = []

    total_cycles = 1000000000
    repeats = 0
    for cycle in range(total_cycles):
        tilt(grid, "N")
        tilt(grid, "W")
        tilt(grid, "S")
        tilt(grid, "E")

        for i_past in reversed(range(cycle)):
            grid_past = patterns[i_past][0]
            if np.all(grid == grid_past):
                logging.warning(f"back to the configuration at {i_past + 1} at cycle {cycle + 1}")
                i_periodic_start = i_past
                i_period = cycle - i_past
                repeats += 1
                break
        if repeats > 0:
            break

        weight = 0
        ii, jj = np.where(grid == "O")
        for i, j in zip(ii, jj):
            w = idim - i
            weight += w
        patterns.append([grid.copy(), weight])
        logging.info(f"{cycle + 1} {weight}")

    print(f"periodicity starts at {i_periodic_start + 1} with the period of {i_period}")

    i_weight = (total_cycles - 1 - i_periodic_start) % i_period + i_periodic_start
    weight = patterns[i_weight][1]
    print(f"weight = {weight}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
