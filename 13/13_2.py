import numpy as np
import sys
import itertools


def read(filename):
    grids = []
    grid = []
    for l in open(filename):
        l = l.strip()
        if len(l) == 0:
            assert grid
            grid = np.array(grid)
            grids.append(grid)
            grid = []
            continue
        grid.append(list(l))
    if grid:
        grid = np.array(grid)
        grids.append(grid)

    return grids


def reflected(grid):
    idim, jdim = grid.shape
    print(grid.shape)

    imirror = 0
    for i in range(1, idim):
        smudge = 0
        mirror = False
        #print(f"is mirror at row {i}?")
        for d in range(1, idim):
            i1 = i - d
            i2 = i + d - 1
            if i1 < 0 or i2 > idim - 1:
                break
            comp = grid[i1, :] == grid[i2, :]
            #print(f"comparing {i1} {i2} {comp}")
            if np.all(comp):
                mirror = True
            elif (~comp).sum() == 1:
                mirror = True
                smudge += 1
                #print("found a smudge")
            else:
                mirror = False
                break
            #if not mirror or smudge > 1:
            #    break
        if mirror and smudge == 1:
            imirror = i
            break

    jmirror = 0
    for j in range(1, jdim):
        smudge = 0
        mirror = False
        print(f"is mirror at col {j}?")
        for d in range(1, jdim):
            j1 = j - d
            j2 = j + d - 1
            if j1 < 0 or j2 > jdim - 1:
                break
            comp = grid[:, j1] == grid[:, j2]
            #print(f"comparing {j1} {j2} {comp}")
            if np.all(comp):
                mirror = True
            elif (~comp).sum() == 1:
                mirror = True
                smudge += 1
                #print("found a smudge")
            else:
                mirror = False
                break
            #if not mirror or smudge > 1:
            #    break
        if mirror and smudge == 1:
            jmirror = j
            break

    return imirror, jmirror

def condensed_print(g):
    for row in g:
        print("".join(row))

def main(filename):
    grids = read(filename)
    sum = 0
    for grid in grids:
        condensed_print(grid)
        row, col = reflected(grid)
        print(row, col)
        p = 100 * row + col
        print(p)
        sum += p
    print(sum)
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
