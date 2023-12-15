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

    boxes = [[] for i in range(256)]
    for s in inst:
        print("inst = ", s)
        if s[-1] == "-":
            label = s[:-1]
            h = hash(label)
            box = boxes[h]
            i0 = None
            print(f"is {label} in {box}?")
            for i, s in enumerate(box):
                print(f"  checking {s} at {i}")
                if s[0] == label:
                    i0 = i
                    break
            if i0 is not None:
                print(f"yes at {i0}")
                box.pop(i0)
        else:
            label, f = s.split("=")
            h = hash(label)
            f = int(f)
            box = boxes[h]
            slot = [i for i in filter(lambda s: s[0] == label, box)]
            if slot:
                assert len(slot) == 1
                slot = slot[0]
                slot[0] = label
                slot[1] = f
            else:
                print("new label and box was ", box)
                box.append([label, f])

        print(label)
        for i, b in enumerate(boxes):
            buf = []
            for slot in b:
                if slot:
                    buf.append(f"{slot[0]} {slot[1]}")
            if buf:
                print(f"box {i:03d}: ", " ".join(buf))

    sum = 0
    for i, box in enumerate(boxes):
        power = 0
        for j, slot in enumerate(box):
            lens = (i + 1) * (j + 1) * slot[1]
            power += lens
        print(f"power of box {i} = {power}")
        sum += power
    print(sum)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
