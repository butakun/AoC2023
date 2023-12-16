import logging
logging.basicConfig(level=logging.WARNING)
import numpy as np


def read(filename):
    return np.array([ list(l.strip()) for l in open(filename) ])


def step(ray, grid, R, init=False):
    ij, direction = ray
    k = ["N", "S", "W", "E"].index(direction)
    if (not init) and R[ij[0], ij[1], k] > 0:
        logging.debug("repeated")
        return []

    if not init:
        R[ij[0], ij[1], k] += 1

    idim, jdim = grid.shape
    if direction == "N":
        if ij[0] == 0:
            logging.debug("stop")
            return []
        ij2 = ij[0] - 1, ij[1]
        if grid[ij2] == "/":
            return [[ij2, "E"]]
        elif grid[ij2] == "\\":
            return [[ij2, "W"]]
        elif grid[ij2] == "-":
            return [[ij2, "E"], [ij2, "W"]]
        elif grid[ij2] == "|" or grid[ij2] == ".":
            return [[ij2, "N"]]
        assert False
    elif direction == "S":
        if ij[0] == idim - 1:
            logging.debug("stop")
            return []
        ij2 = ij[0] + 1, ij[1]
        if grid[ij2] == "/":
            return [[ij2, "W"]]
        elif grid[ij2] == "\\":
            return [[ij2, "E"]]
        elif grid[ij2] == "-":
            return [[ij2, "E"], [ij2, "W"]]
        elif grid[ij2] == "|" or grid[ij2] == ".":
            return [[ij2, "S"]]
        assert False
    elif direction == "W":
        if ij[1] == 0:
            logging.debug("stop")
            return []
        ij2 = ij[0], ij[1] - 1
        if grid[ij2] == "/":
            return [[ij2, "S"]]
        elif grid[ij2] == "\\":
            return [[ij2, "N"]]
        elif grid[ij2] == "-" or grid[ij2] == ".":
            return [[ij2, "W"]]
        elif grid[ij2] == "|":
            return [[ij2, "N"], [ij2, "S"]]
        assert False
    elif direction == "E":
        if ij[1] == jdim - 1:
            logging.debug("stop")
            return []
        ij2 = ij[0], ij[1] + 1
        if grid[ij2] == "/":
            return [[ij2, "N"]]
        elif grid[ij2] == "\\":
            return [[ij2, "S"]]
        elif grid[ij2] == "-" or grid[ij2] == ".":
            return [[ij2, "E"]]
        elif grid[ij2] == "|":
            return [[ij2, "N"], [ij2, "S"]]
        assert False


def energize(ray, grid):
    idim, jdim = grid.shape
    R = np.zeros((idim, jdim, 4), dtype=np.uint32)

    rays = step(ray, grid, R, init=True)
    logging.debug(f"initial rays = {rays}")
    while rays:
        logging.debug(f"{len(rays)}")
        ray = rays.pop(0)
        rays_next = step(ray, grid, R)
        logging.debug(f"ray {ray} -> {rays_next}")
        rays.extend(rays_next)

    E = R.sum(axis=2)
    #print(E)
    energy = np.sum(E > 0)
    return energy


def main(filename):
    grid = read(filename)
    print(grid)
    idim, jdim = grid.shape

    max_energy = 0

    for i in range(idim):
        energy = energize(([i, -1], "E"), grid)
        max_energy = max(energy, max_energy)
        print("E", i, energy, max_energy)

        energy = energize(([i, jdim], "W"), grid)
        max_energy = max(energy, max_energy)
        print("W", i, energy, max_energy)

    for j in range(jdim):
        energy = energize(([-1, j], "S"), grid)
        print("S", j, energy)
        max_energy = max(energy, max_energy)

        energy = energize(([idim, j], "N"), grid)
        print("N", j, energy)
        max_energy = max(energy, max_energy)

    print(max_energy)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
