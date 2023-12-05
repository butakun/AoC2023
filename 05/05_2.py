import re


def read(filename):
    f = open(filename)

    s = [int(x) for x in f.readline().split(": ")[1].split()]
    seed_ranges = []
    for b, e in zip(s[:-1:2], s[1::2]):
        print(b, e, b+e)
        seed_ranges.append((b, b+e))

    f.readline()

    cats = []
    while True:
        try:
            src_cat, dst_cat = f.readline().split()[0].split("-to-")
        except:
            break

        cat2cat = []
        for line in f:
            line = line.strip()
            if not line:
                break
            dst_begin, src_begin, n = [int(x) for x in line.split()]

            translation = (dst_begin, src_begin, n)
            cat2cat.append(translation)

        cats.append(cat2cat)

    return seed_ranges, cats


def cut_range_old(begin, end, dst_begin, src_begin, n):
    src_end = src_begin + n
    cut_begin = max(src_begin, begin)
    cut_end   = min(src_end, end)

    front, center, back = None, None, None
    if cut_end <= cut_begin:
        # no overlap
        if end <= dst_begin:
            front = (begin, end)
        else:
            back = (begin, end)
    else:
        print(f"  cut found {cut_begin}:{cut_end}, {dst_begin}")
        center = (dst_begin + cut_begin - src_begin, dst_begin + cut_end - src_begin)

    if src_begin < cut_begin:
        front = (src_begin, cut_begin)
    if cut_end < src_end:
        back = (cut_end, src_end)

    return front, center, back


def cut_range(r, cutter):
    cut_begin = max(cutter[0], r[0])
    cut_end   = min(cutter[1], r[1])

    front, center, back = None, None, None
    if cut_end <= cut_begin:
        # no overlap
        if r[1] <= cutter[0]:
            front = r
        else:
            back = r
    else:
        center = (cut_begin, cut_end), (cut_begin + cutter[2], cut_end + cutter[2])

        if r[0] < cut_begin:
            front = (r[0], cut_begin)
        if cut_end < r[1]:
            back = (cut_end, r[1])

    return front, center, back


def overlaps(begin_1, end_1, begin_2, end_2):
    return begin1 < end2 and begin2 < end1 


def single(seed, cats):
    fr = seed
    to = seed
    for cat2cat in cats:
        for dst_begin, src_begin, n in cat2cat:
            if src_begin <= to and to < src_begin + n:
                to = dst_begin + (to - src_begin)
                break
    return to


def brute_force(seed_ranges, cats):
    lowest = seed_ranges[0][0]
    for seed_range in seed_ranges:
        print("seed rangs ", seed_range)
        for seed in range(seed_range[0], seed_range[1]):
            low = single(seed, cats)
            #print(seed, low)
            lowest = min(lowest, single(seed, cats))
    print(lowest)


def main(filename):
    seed_ranges, cats = read(filename)
    #brute_force(seed_ranges, cats)
    #return

    seed_ranges = sorted(seed_ranges, key=lambda v: v[0])

    cats_ = []
    for i, cat2cat in enumerate(cats):
        src_ranges = sorted(cat2cat, key=lambda v: v[1])  # sorted by src_begin
        cats_.append(src_ranges)

    steps = []
    for cat in cats_:
        cutters = []  # begin, end, offset
        for dst_begin, src_begin, n in cat:
            cutter = src_begin, src_begin+n, dst_begin - src_begin
            cutters.append(cutter)
        steps.append(cutters)

    print(seed_ranges)
    print(steps)

    all_res = []
    for seed_range in seed_ranges:
        range_bits = [seed_range]
        for i, step in enumerate(steps):
            print("=" * 10)
            print(f"Step {i}: range_bits = {range_bits}, cutters = {step}")
            res = []
            while range_bits:
                print(f"  cutting range_bits = {range_bits}")
                cut = False
                bit = range_bits.pop(0)
                num_cutters = len(step)
                for j, cutter in enumerate(step):
                    front, center, back = cut_range(bit, cutter)
                    print(f"range {bit} cut by {cutter}")
                    print(f"  {front}, {center}, {back}")
                    if center:
                        res.append(center[1])
                        cut = True
                        if front and j == 0:
                            res.append(front)
                        if back:
                            #range_bits.insert(0, back)
                            bit = back
                            if j == (num_cutters - 1):
                                res.append(bit)
                if not cut:
                    print(f"no cut performed, bit = {bit}")
                    res.append(bit)
                    #break
            range_bits = sorted(res, key=lambda v: v[0])
            print(f"  Step {i} done: range_bits = {range_bits}")

        print(f"  Result for seed range {seed_range}: {range_bits}")
        all_res.extend(range_bits.copy())
        print(f"*** finished processing seed_range {seed_range}, range_bits = {range_bits}")

    all_res = sorted(all_res, key=lambda v: v[0])
    print(all_res)
    lowest = all_res[0][0]
    print(f"lowest = {lowest}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
