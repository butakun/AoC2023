import logging
logging.basicConfig(level=logging.DEBUG)
import numpy as np


def read(filename):
    plan = [ l.strip().split(" ") for l in open(filename) ]
    plan = [ (l[0], int(l[1]), l[2][2:-1]) for l in plan ]
    return plan


def main(filename, method):
    plan = read(filename)
    #print(plan)

    holes = set()
    i, j = 0, 0
    holes.add((i, j))
    imin, imax, jmin, jmax = i, i, j, j
    for direction, blocks, _ in plan:
        if direction == "U":
            di, dj = -1,  0
        elif direction == "D":
            di, dj =  1,  0
        elif direction == "L":
            di, dj =  0, -1
        elif direction == "R":
            di, dj =  0,  1
        else:
            assert False
        for k in range(blocks):
            i += di
            j += dj
            holes.add((i, j))
            imax = max(i, imax)
            jmax = max(j, jmax)
            imin = min(i, imin)
            jmin = min(j, jmin)

    print(len(holes))

    # find an interior point
    start = None
    for i, j in holes:
        if (i, j-1) not in holes and (i, j+1) not in holes:
            outside = True
            for jm in range(j):
                if (i, jm) in holes:
                    outside = False
                    break
            if outside:
                start = (i, j+1)
                break

    assert start is not None
    print("interior point = ", start)

    nodes = [start]
    lag = {start}
    while nodes:
        node = nodes.pop(0)
        i, j = node
        for nei in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            if (nei not in holes) and (nei not in lag):
                lag.add(nei)
                nodes.append(nei)

    for i in range(imin, imax + 1):
        buf = ""
        for j in range(jmin, jmax + 1):
            if (i, j) in holes:
                buf += "#"
            elif (i, j) in lag:
                buf += "+"
            else:
                buf += "."
        print(buf)

    print(len(lag))
    print(len(holes) + len(lag))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    parser.add_argument("--method", default="dijkstra")
    args = parser.parse_args()
    main(args.input, args.method)
