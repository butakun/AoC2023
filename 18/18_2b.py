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


def main(filename, noswap):
    plan = read(filename)
    if not noswap:
        plan = decipher(plan)

    trench = []
    ij1 = 0, 0
    border = 0
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
        border += blocks

        ij2 = ij1[0] + di, ij1[1] + dj
        trench.append((ij1, ij2))
        ij1 = ij2

    A = 0
    for ij1, ij2 in trench:
        a = ij1[0] * ij2[1] - ij1[1] * ij2[0]
        A += a
    A /= 2
    total = abs(A) + border / 2 + 1
    total = int(total)
    print(f"A = {A}, border = {border}, total = {total}")
    return


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    parser.add_argument("--noswap", action="store_true")
    args = parser.parse_args()
    main(args.input, args.noswap)
