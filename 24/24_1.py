import logging
logging.basicConfig(level=logging.INFO)
from itertools import combinations
import numpy as np


def read(filename):
    stones = []
    for l in open(filename):
        pp, vv = l.strip().split("@")
        pp = [int(p) for p in pp.split(",")]
        vv = [int(v) for v in vv.split(",")]
        pp = np.array(pp)
        vv = np.array(vv)
        stones.append((pp, vv))
    return stones


def cross_prod(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]


def intersection(s1, s2):
    p1, v1 = s1
    p2, v2 = s2
    # p1 + t1 * v1 = p2 + t2 * v2
    # p1 x v2 + t1 * (v1 x v2) = p2 x v2 + t2 * (v2 x v2)
    # p1 x v2 + t1 * (v1 x v2) = p2 x v2
    # t1 * (v1 x v2) = (p2 - p1) x v2
    # t1 * (v1 x v2).k = ((p2 - p1) x v2).k
    # t1 = (((p2 - p1) x v2).k) / ((v1 x v2).k)

    v12 = p2 - p1
    v12xv2 = cross_prod(v12, v2)
    v1xv2 = cross_prod(v1, v2)
    if v1xv2 == 0:
        return None, None, None, None
    t1 = v12xv2 / v1xv2
    p1c = p1 + t1 * v1

    if v2[0] != 0:
        t2 = (p1c - p2)[0] / v2[0]
    elif v2[1] != 0:
        t2 = (p1c - p2)[1] / v2[1]
    else:
        t2 = (p1c - p2)[2] / v2[2]

    p2c = p2 + t2 * v2

    return t1, p1c, t2, p2c


def main(filename):
    stones = read(filename)
    print(stones)

    count = 0
    if False:
        xmin, xmax = 7, 27
        ymin, ymax = 7, 27
    else:
        xmin, xmax = 200000000000000, 400000000000000
        ymin, ymax = 200000000000000, 400000000000000

    for s1, s2 in combinations(stones, 2):
        t1, pc1, t2, pc2 = intersection(s1, s2)
        if t1 is None:
            inside = False
        elif t1 > 0 and t2 > 0:
            x, y = pc1[0], pc2[1]
            inside = (xmin <= x) and (x <= xmax) and (ymin <= y) and (y <= ymax)
            if inside:
                count += 1
        else:
            inside = False
        #print(f"testing {s1[0]}, {s2[0]}")
        print(t1, pc1, t2, pc2, inside)
    print(count)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
