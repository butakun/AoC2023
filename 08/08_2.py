import numpy as np


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


def traverse_one(node_start, inst, network):

    goals = []
    node = node_start
    steps = 0
    while True:
        i = steps % len(inst)

        if node[2] == "Z":
            print(" * ", node, steps, i)
            goals.append(steps)
            if True or len(goals) > 3:
                break

        which = inst[i]
        left, right = network[node]
        #print(f"  {node} -> {left}-{right} {i} {len(inst)}")
        if which == "L":
            node = left
        elif which == "R":
            node = right

        if i == 0 and node == node_start:
            break

        steps += 1

    return goals, steps


def main(filename):
    inst, network = read(filename)
    print(inst)
    print(network)

    ints = []
    for node in network:
        if node[2] == "A":
            goals, steps = traverse_one(node, inst, network)
            print(f"NODE {node} -> {goals}, {steps}")
            ints.append(goals[0])

    lcm = np.lcm.reduce(ints)
    print(lcm)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
