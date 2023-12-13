import numpy as np
import sys
import itertools


def read(filename):
    lines = [l.strip().split() for l in open(filename)]
    records = [[np.array(list(l[0])), [int(i) for i in l[1].split(",")]] for l in lines]
    return records


def good(pat, strips):
    buf = "".join(pat)
    buf = buf.split(".")
    buf = [b for b in buf if b]
    if len(buf) != len(strips):
        return False
    runs = np.array([len(b) for b in buf])
    strips = np.array(strips)
    if np.any(runs != strips):
        return False
    print("good = ", runs, strips)
    return True


def main(filename):
    records = read(filename)
    print(records)

    sum = 0
    for pat, strips in records:
        indices = np.where(pat == "?")[0]
        print(pat, indices)
        n_bits = indices.shape[0]
        count = 0
        for p in range(pow(2, n_bits)):
            p_ = f"{p:0{n_bits}b}"
            p_ = p_.replace("0", ".")
            p_ = p_.replace("1", "#")
            p_ = np.array(list(p_))
            pat_ = pat.copy()
            pat_[indices] = p_
            if good(pat_, strips):
                print(p_, pat_)
                count += 1
        print("count = ", count)
        sum += count
    print(sum)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
