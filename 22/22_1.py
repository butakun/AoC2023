import logging
logging.basicConfig(level=logging.INFO)
import numpy as np
from collections import defaultdict


def read(filename):
    bricks = []
    for l in open(filename):
        brick = [ [c for c in map(int, t.split(","))] for t in l.strip().split("~") ]
        bricks.append(np.array(brick))
    return bricks


def dump_grid(grid):
    xdim, ydim, zdim = grid.shape
    for z in reversed(range(zdim)):
        row = grid[:, :, z]
        raise NotImplementedError


def fall(grid, bid, brick):
    p1, p2 = brick

    xmin, ymin, zbot = brick.min(axis=0)
    xmax, ymax, ztop = brick.max(axis=0)
    dz = ztop - zbot + 1
    #print(xmin, ymin, zbot)
    #print(xmax, ymax, ztop, dz)

    zset = zbot
    for z in reversed(range(1, zbot)):
        obs = grid[xmin:xmax+1,ymin:ymax+1,z] == 0
        if np.all(obs):
            zset = z
        else:
            break
    print(f"brick {bid} : ({xmin},{ymin})-({xmax},{ymax})-({zbot}-{ztop}) falls to {zset}")

    grid[xmin:xmax+1, ymin:ymax+1, zset:zset+dz] = bid


def main(filename):
    bricks = read(filename)

    bricks.sort(key=lambda b: min(b[0,2], b[1,2]))
    for i, brick in enumerate(bricks):
        bid = i + 1
        print(f"brick {bid}: {brick[0,:]}-{brick[1,:]}")

    xmax, ymax, zmax = bricks[0][0]
    for p1, p2 in bricks:
        xmax = max(xmax, p1[0], p2[0])
        ymax = max(ymax, p1[1], p2[1])
        zmax = max(zmax, p1[2], p2[2])

    grid = np.zeros((xmax+1, ymax+1, zmax+1), np.int32)

    print(grid)

    for i, brick in enumerate(bricks):
        bid = i + 1
        fall(grid, bid, brick)

    # build supports tree and supportedby tree
    removed = set()
    supports = defaultdict(list)
    supported = defaultdict(list)
    for bid in range(1, len(bricks)+1):
        brick = bricks[bid - 1]
        xmin, ymin, _ = brick.min(axis=0)
        xmax, ymax, _ = brick.max(axis=0)
        xx, yy, zz = np.where(grid == bid)
        print(f"brick = {bid}")
        print(xx, yy, zz)
        rests = set()
        for x, y, z in zip(xx, yy, zz):
            above = grid[x, y, z+1]
            print(f"  {x},{y},{z+1} -> {above}")
            if above != bid and above != 0:
                rests.add(above)
        print(f"  {rests} are on top")
        supports[bid] = rests
        for ab in rests:
            supported[ab].append(bid)

    print(supports)
    print(supported)

    canberemoved = set()
    for a, bb in supports.items():
        bb_ = bb.copy()
        for b in bb:
            supported_by_others = False
            for c in supported[b]:
                if c != a:
                    supported_by_others = True
                    break
            if supported_by_others:
                bb_.remove(b)
        if len(bb_) == 0:
            canberemoved.add(a)

    print(canberemoved)
    print(len(canberemoved))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
