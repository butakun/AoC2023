def read(filename):
    inst = []
    for l in open(filename):
        inst += l.strip().split(",")
    return inst


def hash(s):
    v = 0
    for c in s:
        v += ord(c)
        v *= 17
        v = v % 256
    return v


def main(filename):
    inst = read(filename)
    print(inst)

    sum = 0
    for s in inst:
        h = hash(s)
        sum += h
        print(s, h)
    print(sum)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
