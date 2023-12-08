from functools import cmp_to_key


def read(filename):
    f = open(filename)
    inst = f.readline().strip()
    inst = list(inst)

    f.readline()

    network = {}
    for line in f:
        tokens = line.split()
        node = tokens[0]
        left = tokens[2].strip("(),")
        right = tokens[3].strip("(),")
        network[node] = (left, right)

    return inst, network


def traverse_(node, index, inst, network):
    print(f"node = {node}")
    if node == "ZZZ":
        return index

    i = index % len(inst)
    which = inst[i]

    left, right = network[node]
    print(f"  -> {left} <-> {right}")
    if which == "L":
        return traverse(left, index+1, inst, network)
    elif which == "R":
        return traverse(right, index+1, inst, network)


def traverse(node, index, inst, network):

    node = "AAA"
    steps = 0

    while node != "ZZZ":
        i = steps % len(inst)
        which = inst[i]
        left, right = network[node]
        if which == "L":
            node = left
        elif which == "R":
            node = right
        steps += 1

    return steps

def main(filename):
    inst, network = read(filename)
    print(inst)
    print(network)

    print("START")
    steps = traverse("AAA", 0, inst, network)
    print(steps)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
