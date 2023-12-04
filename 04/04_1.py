import re


def read(filename):
    spaces = re.compile(r"\s+")
    cards = []
    for line in open(filename):
        line = line.strip()
        line = re.sub(spaces, " ", line)
        winners, numbers = line.split(": ")[1].split(" | ")
        winners = [int(x) for x in winners.strip().split(" ")]
        numbers = [int(x) for x in numbers.strip().split(" ")]
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
