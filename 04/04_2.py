import numpy as np


def read(filename):
    cards = []
    for line in open(filename):
        line = line.strip()
        card_number, contents = line.split(": ")
        card_number = [x for x in card_number.strip().split(" ") if x][1]
        card_number = int(card_number)
        winners, numbers = contents.split(" | ")
        winners = [x for x in winners.strip().split(" ") if x]
        numbers = [x for x in numbers.strip().split(" ") if x]
        winners = [int(x) for x in winners]
        numbers = [int(x) for x in numbers]
        cards.append((card_number, winners, numbers))
    return cards


def main(filename):
    cards = read(filename)
    print(cards)

    wins = {}
    for card_number, winners, numbers in cards:
        found = [ number in winners for number in numbers ]
        count = sum(found)
        wins[card_number] = count
    print(wins)

    pile = {card_number: 1 for card_number, _, _ in cards}
    for card_number, _, _ in cards:
        copies = pile[card_number]
        count = wins[card_number]
        for i in range(card_number + 1, card_number + 1 + count):
            if i in pile:
                pile[i] += copies
            else:
                break
        print(f"card {card_number}: pile {pile}")

    num_cards = sum(pile.values())
    print(num_cards)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
