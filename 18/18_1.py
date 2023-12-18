import logging
logging.basicConfig(level=logging.DEBUG)
import numpy as np


def read(filename):
    plan = [ l.strip().split(" ") for l in open(filename) ]
    plan = [ (l[0], int(l[1]), l[2][2:-1]) for l in plan ]
    return plan


def main(filename, method):
    plan = read(filename)
    print(plan)

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

    start = (-146, 147)
    #start = (1, 1)
    nodes = [start]
    lag = {start}
    while nodes:
        node = nodes.pop(0)
        i, j = node
        print(f"node = {i}, {j}")
        for nei in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            print(f"nei = {nei}, {nei not in holes}, {nei not in lag}")
            if (nei not in holes) and (nei not in lag):
                print(f"adding {nei}")
                lag.add(nei)
                nodes.append(nei)
            else:
                print(f"skpping {nei}")

    print(len(lag))
    print(len(holes) + len(lag))

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


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    parser.add_argument("--method", default="dijkstra")
    args = parser.parse_args()
    main(args.input, args.method)
