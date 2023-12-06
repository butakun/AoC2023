import math


def read(filename):
    f = open(filename)

    Ts = [int(T) for T in f.readline().strip().split()[1:]]
    Ds = [int(T) for T in f.readline().strip().split()[1:]]

    races = [{"T": T, "D": D} for T, D in zip(Ts, Ds)]
    return races


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
    races = read(filename)
    print(races)

    product = 1
    for race in races:
        n = do_race(**race)
        product *= n
        print(n)
    print(product)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
