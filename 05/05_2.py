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


def cut_a_range_with_cutters(r, cutters):
    ranges = [r]
    res = []
    while ranges:
        rr = ranges.pop(0)
        for cutter in cutters:
            if not rr:
                break
            if cutter[1] <= rr[0]:
                continue
            front, center, back = cut_range(rr, cutter)
            if center:
                if front:
                    res.insert(0, front)
                res.append(center[1])
                if back:
                    rr = back
                else:
                    rr = None
            else:
                rr = None
        if rr:
            res.append(rr)
    return res


def test1():
    r = [90, 99]
    cutters = [[56, 93, 4], [93, 97, -37]]

    res = cut_a_range_with_cutters(r, cutters)
    print(res)


def follow_a_range(seed_range, steps):
    ranges = [seed_range]
    for i, step in enumerate(steps):
        #print(f"Step {i}: ranges = {ranges}, cutters = {step}")

        next_ranges = []
        for seed_range in ranges:
            remnants = cut_a_range_with_cutters(seed_range, step)
            next_ranges.extend(remnants)

        #print(f"Step {i} DONE: next_ranges = {next_ranges}")
        ranges = next_ranges
    return ranges


def main(filename):
    seed_ranges, cats = read(filename)

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

    final_ranges = []
    for r in seed_ranges:
        next_ = follow_a_range(r, steps)
        final_ranges.extend(next_)

    final_ranges = sorted(final_ranges, key=lambda r: r[0])
    print(final_ranges)
    lowest = final_ranges[0][0]
    print("lowest = ", lowest)
    return


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
