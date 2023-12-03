def read(filename):
    numbers = []
    stars = []
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
                if c == "*":
                    stars.append((c, (i, j)))
        if number:
            numbers.append((number, (i, len(line) - len(number))))

    return numbers, stars


def main(filename):
    numbers, stars = read(filename)
    print("NUMBERS")
    print(numbers)
    print("STARS")
    print(stars)

    ratios = []
    for star, (i, j) in stars:
        cogs = []
        for number, (ii, jj) in numbers:
            imin = ii - 1
            imax = ii + 1
            jmin = jj - 1
            jmax = jj + len(number)
            if imin <= i and i <= imax and jmin <= j and j <= jmax:
                cogs.append((int(number), (ii,jj)))
                if len(cogs) > 2:
                    break
        if len(cogs) == 2:
            buf = f"* at ({i},{j}) connects "
            for teeth, (ii, jj) in cogs:
                buf += f"{teeth} in ({ii},{jj}) "
            print(buf)

            ratios.append(cogs[0][0] * cogs[1][0])

    print(ratios)
    print(sum(ratios))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
