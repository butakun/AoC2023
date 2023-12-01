import numpy as np

words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
word2digit = { w: str(i) for i, w in enumerate(words) }


def first(line):
    digits = [ i for i, c in enumerate(line) if c.isdigit() ]
    if digits:
        first_digit_index = digits[0]
    else:
        first_digit_index = None

    min_index = len(line) + 1
    min_word = None
    for w in word2digit:
        try:
            i = line.index(w)
        except:
            continue
        if i < min_index:
            min_index = i
            min_word = w
    first_digit = None
    if min_word is None:
        first_digit = int(line[first_digit_index])
    else:
        if min_index < first_digit_index:
            first_digit = word2digit[min_word]
        else:
            first_digit = int(line[first_digit_index])
    return first_digit


def last(line):
    digits = [ i for i, c in enumerate(line) if c.isdigit() ]
    if digits:
        last_digit_index = digits[-1]
    else:
        last_digit_index = None

    max_index = -1
    max_word = None
    for sublen in range(1, len(line)):
        sub = line[-sublen:]
        for w in word2digit:
            if sub.startswith(w):
                max_index = len(line) - sublen
                max_word = w
                break

        if max_word:
            break

    """
    print("last_digit_index = ", last_digit_index)
    print("max index = ", max_index)
    print("max word = ", max_word)
    """
    last_digit = None
    if max_word is None:
        last_digit = int(line[last_digit_index])
    else:
        if max_index > last_digit_index:
            last_digit = word2digit[max_word]
        else:
            last_digit = int(line[last_digit_index])
    return last_digit


def main(filename):
    if False:
        line = "5fivezgfgcxbf3five"
        line = "sixseven9jgpnxqhq"
        line = "3oneeighttwo"
        f = first(line)
        l = last(line)
        value = int(f"{f}{l}")
        print(line, f, l, value)
        return

    lines = [ l.strip() for l in open(filename) ]

    print(word2digit)

    values = []
    for line in lines:
        f = first(line)
        l = last(line)
        value = int(f"{f}{l}")
        print(line, f, l, value)
        
        values.append(value)

    values = np.array(values)
    print(values)
    print(values.sum())


if __name__ == "__main__":
    main("input.txt")
