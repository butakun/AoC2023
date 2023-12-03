def read(filename):
    numbers = []
    symbols = []
    for i, line in enumerate(open(filename)):
        line = line.strip()
        number = ""
        for j, c in enumerate(line):
            if c.isdigit():
                number += c
            else:
                if len(number) > 0:
                    numbers.append((number, (i, j - len(number))))
                    number = ""
                if c != ".":
                    symbols.append((c, (i, j)))
        if number:
            numbers.append((number, (i, len(line) - len(number))))

    return numbers, symbols


def main(filename):
    numbers, symbols = read(filename)
    print("NUMBERS")
    print(numbers)
    print("SYMBOLS")
    print(symbols)

    parts = []
    for number, (i, j) in numbers:
        imin = i - 1
        imax = i + 1
        jmin = j - 1
        jmax = j + len(number)
        for symbol, (ii, jj) in symbols:
            if imin <= ii and ii <= imax and jmin <= jj and jj <= jmax:
                #print(f"{symbol} at ({ii},{jj}) is adjacent to {number} at ({i},{j}), ({imin}:{imax}, {jmin}:{jmax})")
                print(f"{number} at ({i},{j}) adjacent to {symbol} in ({ii},{jj})")
                parts.append(int(number))
                break

    print(parts)
    print(sum(parts))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
