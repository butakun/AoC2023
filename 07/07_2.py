from functools import cmp_to_key


def read(filename):
    hands_bids = [l.strip().split() for l in open(filename)]
    hands_bids = [[h, int(b)] for h, b in hands_bids]
    return hands_bids


def kind(h):
    uniqs = list(set(h))

    jokers = h.count("J")
    if jokers > 0:
        uniqs.remove("J")
        l = len(uniqs)
        if l == 0:
            # five of a kind
            return 6
        elif l == 1:
            # four of a kind -> five of a kind
            return 6
        elif l == 2:
            count1 = h.count(uniqs[0])
            count2 = h.count(uniqs[1])
            if count1 == 3 or count2 == 3:
                # three of a kind -> four of a kind
                return 5
            elif count1 == 2 and count2 == 2:
                # two pairs -> full house
                return 4
            elif count1 == 1 or count2 == 1:
                if jokers == 1:
                    # three of a kind -> four of a kind
                    assert count1 == 3 or count2 == 3
                    return 5
                elif jokers == 2:
                    # two of a kind -> four of a kind
                    assert count1 == 2 or count2 == 2
                    return 5
                elif jokers == 3:
                    # high card -> four of a kind
                    return 5
                else:
                    assert False
        elif l == 3:
            count1 = h.count(uniqs[0])
            count2 = h.count(uniqs[1])
            count3 = h.count(uniqs[2])
            if jokers == 1:
                # one pair -> three of a kind
                return 3
            elif jokers == 2:
                # high card -> three of a kind
                return 3
            else:
                assert False
        elif l == 4:
            # high card -> one pair
            assert jokers == 1
            return 1

    l = len(uniqs)
    if l == 5:  # high card
        return 0
    elif l == 4:  # one pair
        return 1
    elif l == 3:
        if h.count(uniqs[0]) == 3 or h.count(uniqs[1]) == 3 or h.count(uniqs[2]) == 3:
            # three of a kind
            return 3
        else:
            # two pair
            return 2
    elif l == 2:
        c = h.count(uniqs[0])
        if c == 3 or c == 2:
            # full house
            return 4
        else:
            # four of a kind
            return 5
    else:
        return 6


def cmp_cards(c1, c2):
    cards = "J23456789TJQKA"
    i1 = cards.index(c1) 
    i2 = cards.index(c2) 
    if i1 < i2:
        return -1
    elif i2 < i1:
        return 1
    else:
        return 0


def compare(h1, h2):
    k1, k2 = kind(h1), kind(h2)
    print(f"compare: {h1}, {h2}, {k1}, {k2}")
    if k1 < k2:
        return -1
    elif k2 < k1:
        return 1
    else:
        for c1, c2 in zip(h1, h2):
            c = cmp_cards(c1, c2)
            if c == 0:
                continue
            return c


def main(filename):
    hands_bids = read(filename)
    print(hands_bids)

    hands = [h for h, _ in hands_bids]
    print(hands)
    bids = {h: b for h, b in hands_bids}

    hands = sorted(hands, key=cmp_to_key(compare))
    print(hands)

    sum = 0
    for rank, hand in enumerate(hands):
        rank = rank + 1
        point = bids[hand] * rank
        sum += point
        print(f"{hand} = {point} points as rank {rank}")

    print(sum)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
