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


def left_right(ij1, ij2, imin, imax, jmin, jmax):
    # trench contained in left
    i1, j1 = ij1
    i2, j2 = ij2
    if i1 == i2:
        if j1 < j2:
            # 1---->2
            left  = ((imin, j1), (i1, j2))
            right = ((i1+1, j1), (imax, j2))
        else:
            # 2<----1
            left  = ((i1, j2), (imax, j1))
            right = ((imin, j2), (i1-1, j1))
    elif j1 == j2:
        if i1 < i2:
            # 1
            # v
            # 2
            left  = ((i1, j1+1), (i2, jmax))
            right = ((i1, jmin), (i2, j1))
        else:
            # 2
            # ^
            # 1
            left  = ((i2, jmin), (i1, j1))
            right = ((i2, j1+1), (i2, jmax))
    else:
        raise ValueError

    return left, right


def intersect_1d(r1, r2):
    s1 = max(r1[0], r2[0])
    s2 = min(r1[1], r2[1])
    if s1 < s2:
        return s1, s2
    else:
        return None, None


def intersect_2d(a, b):
    i1, i2 = intersect_1d((a[0][0], a[1][0]), (b[0][0], b[1][0]))
    j1, j2 = intersect_1d((a[0][1], a[1][1]), (b[0][1], b[1][1]))
    if i1 is None or j1 is None:
        return None
    else:
        return ((i1, j1), (i2, j2))


def compressed_print(x):
    for row in x:
        buf = "".join([f"{int(v)}" for v in row])
        print(buf)


def main(filename, method):
    plan = read(filename)
    plan = decipher(plan)
    print(plan)

    trench = []
    i, j = 0, 0
    i_knots, j_knots = {i}, {j}
    imin, imax, jmin, jmax = i, i, j, j
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

        imin = min(i2, imin)
        jmin = min(j2, jmin)
        imax = max(i2, imax)
        jmax = max(j2, jmax)

        i, j = i2, j2

    print(imin, imax, jmin, jmax)
    idim = imax-imin+1
    jdim = jmax-jmin+1

    i_knots = sorted(i_knots)
    j_knots = sorted(j_knots)
    print(i_knots, j_knots)

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

    print("END")
    #print(cells)
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
    parser.add_argument("--method", default="dijkstra")
    args = parser.parse_args()
    main(args.input, args.method)
