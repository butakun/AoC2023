import re


def read(filename):
    f = open(filename)

    seeds = [int(x) for x in f.readline().split(": ")[1].split()]
    print(seeds)
    f.readline()

    cats = []
    while True:
        try:
            src_cat, dst_cat = f.readline().split()[0].split("-to-")
        except:
            break
        print(src_cat, dst_cat)

        cat2cat = []
        for line in f:
            line = line.strip()
            if not line:
                break
            dst_begin, src_begin, n = [int(x) for x in line.split()]
            print(dst_begin, src_begin, n)

            translation = (dst_begin, src_begin, n)
            cat2cat.append(translation)

        cats.append(cat2cat)

    return seeds, cats


def main(filename):
    seeds, cats = read(filename)
    print(seeds)
    print(cats)

    lowest = seeds[0]
    for seed in seeds:
        fr = seed
        to = seed
        print(f"seed {fr}")
        for cat2cat in cats:
            for dst_begin, src_begin, n in cat2cat:
                print(f"test {dst_begin}, {src_begin}, {n}")
                if src_begin <= to and to < src_begin + n:
                    print(f"{src_begin} <= {to} < {src_begin + n}")
                    to = dst_begin + (to - src_begin)
                    break
            print(f" -> {to}")

        lowest = min(to, lowest)

    print(lowest)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
