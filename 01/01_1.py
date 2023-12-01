def main(filename):
    lines = [ l.strip() for l in open(filename) ]

    values = []
    for line in lines:
        digits = [ c for c in line if c.isdigit() ]
        value = int(digits[0] + digits[-1])
        values.append(value)

    print(values)
    print(sum(values))


if __name__ == "__main__":
    main("input.txt")
