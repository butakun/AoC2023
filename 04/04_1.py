import numpy as np


def read(filename):
    cards = []
    for line in open(filename):
        line = line.strip()
        winners, numbers = line.split(": ")[1].split(" | ")
        winners = [x for x in winners.strip().split(" ") if x]
        numbers = [x for x in numbers.strip().split(" ") if x]
        winners = [int(x) for x in winners]
        numbers = [int(x) for x in numbers]
        cards.append((winners, numbers))
    return cards


def main(filename):
    cards = read(filename)
    print(cards)

    points = []
    for winners, numbers in cards:
        found = [ number in winners for number in numbers ]
        count = sum(found)
        if count == 0:
            point = 0
        else:
            point = pow(2, count-1)
        print(point)
        points.append(point)

    print(sum(points))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
