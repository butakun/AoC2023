def main(filename):
    lines = [ l.strip() for l in open(filename) ]

    sum = 0
    for line in lines:
        digits = [ c for c in line if c.isdigit() ]
        value = int(digits[0] + digits[-1])
        sum += value

    print(sum)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
