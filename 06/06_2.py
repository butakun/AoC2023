import math


def read(filename):
    f = open(filename)

    T = int(f.readline().split(":")[1].replace(" ", "").strip())
    D = int(f.readline().split(":")[1].replace(" ", "").strip())

    return T, D


def do_race(T, D):
    D = D + 1
    det = math.sqrt(T * T - 4 * D)
    tb_min = (T - det) / 2
    tb_max = (T + det) / 2
    print(tb_min, tb_max)
    tb_min = math.ceil(tb_min)
    tb_max = math.floor(tb_max)
    print(tb_min, tb_max)

    return int((tb_max + 1) - tb_min)

def main(filename):
    T, D = read(filename)
    print(T, D)

    n = do_race(T, D)
    print(n)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
