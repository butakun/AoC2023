import logging
logging.basicConfig(level=logging.DEBUG)
import numpy as np


def read(filename):
    plan = [ l.strip().split(" ") for l in open(filename) ]
    plan = [ (l[0], int(l[1]), l[2][2:-1]) for l in plan ]
    return plan


def decipher(plan):
    deciphered = []
    for _, _, code in plan:
        blocks = int(code[:5], 16)
        d = int(code[5])
        if d == 0:
            direction = "R"
        elif d == 1:
            direction = "D"
        elif d == 2:
            direction = "L"
        elif d == 3:
            direction = "U"
        else:
            raise ValueError
        deciphered.append((direction, blocks))
    return deciphered


def compressed_print(x):
    for row in x:
        buf = "".join([f"{int(v)}" for v in row])
        print(buf)


def main(filename):
    plan = read(filename)
    plan = decipher(plan)
    print(plan)

    trench = []
    i, j = 0, 0
    i_knots, j_knots = {i}, {j}
    for inst in plan:
        direction, blocks = inst[0], inst[1]
        if direction == "U":
            di, dj = -blocks,  0
        elif direction == "D":
            di, dj =  blocks,  0
        elif direction == "L":
            di, dj =  0, -blocks
        elif direction == "R":
            di, dj =  0,  blocks
        else:
            assert False

        ij1 = i, j
        i2 = i + di
        j2 = j + dj
        ij2 = i2, j2

        trench.append((ij1, ij2))
        i_knots.add(i2)
        j_knots.add(j2)
        print(f"adding knots {i2}, {j2}")

        i, j = i2, j2

    i_knots = sorted(i_knots)
    j_knots = sorted(j_knots)
    print(i_knots, j_knots)

    imin, imax = min(i_knots), max(i_knots)
    jmin, jmax = min(j_knots), max(j_knots)

    print(imin, imax, jmin, jmax)
    idim = imax-imin+1
    jdim = jmax-jmin+1

    gidim = len(i_knots)
    gjdim = len(j_knots)
    cells = np.zeros((gidim-1, gjdim-1), dtype=np.int32)
    #grid = np.zeros((idim,jdim), dtype=np.uint8)

    for ij1, ij2 in trench:
        gi1 = i_knots.index(ij1[0])
        gi2 = i_knots.index(ij2[0])
        gj1 = j_knots.index(ij1[1])
        gj2 = j_knots.index(ij2[1])
        if gi1 == gi2:
            if gj1 < gj2:
                cells[   :gi1  , gj1:gj2] += 1  # left
                cells[gi1:     , gj1:gj2] -= 1  # right
            elif gj2 < gj1:
                cells[gi1:     , gj2:gj1] += 1  # left
                cells[   :gi1  , gj2:gj1] -= 1  # right
            else:
                raise ValueError
        elif gj1 == gj2:
            if gi1 < gi2:
                cells[gi1:gi2, gj1:] += 1  # left
                cells[gi1:gi2, :gj1] -= 1  # right
            elif gi2 < gi1:
                cells[gi2:gi1, :gj1] += 1  # left
                cells[gi2:gi1, gj1:] -= 1  # right
            else:
                raise ValueError
        else:
            raise ValueError

    compressed_print((cells != 0))
    print(np.unique(cells))

    total = 0
    for gi in range(gidim-1):
        for gj in range(gjdim-1):
            if cells[gi, gj] == 0:
                continue
            i1 = i_knots[gi]
            j1 = j_knots[gj]
            i2 = i_knots[gi+1]
            j2 = j_knots[gj+1]
            area = (i2 - i1 + 1) * (j2 - j1 + 1)
            total += area

    for gi in range(gidim-1):
        for gj in range(gjdim-2):
            j = j_knots[gj+1]
            if cells[gi, gj] != 0 and cells[gi, gj+1] != 0:
                i1 = i_knots[gi]
                i2 = i_knots[gi+1]
                total -= i2 - i1 + 1
    for gj in range(gjdim-1):
        for gi in range(gidim-2):
            i = i_knots[gi+1]
            if cells[gi, gj] != 0 and cells[gi+1, gj] != 0:
                j1 = j_knots[gj]
                j2 = j_knots[gj+1]
                total -= j2 - j1 + 1

    for gi in range(gidim-2):
        for gj in range(gjdim-2):
            if cells[gi, gj] != 0 and cells[gi+1, gj] != 0 and cells[gi,gj+1] != 0 and cells[gi+1,gj+1] != 0:
                total += 1

    print(total)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
