words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
word2digit = {w: d for w, d in zip(words, range(1, 10))}
digit2word = {str(d): w for w, d in word2digit.items()}

word2digit_r = {w[::-1]: d for w, d in word2digit.items()}


def first(line, w2d):
    index = len(line)
    digit = None
    for w, d in w2d.items():
        try:
            found = line.index(w)
            if found < index:
                index = found
                digit = d
        except:
            continue

    return digit


def main(filename):
    lines = [ l.strip() for l in open(filename) ]

    values = []
    for line in lines:
        words = line
        for d, w in digit2word.items():
            words = words.replace(d, w)
        words_r = words[::-1]

        f = first(words, word2digit)
        l = first(words_r, word2digit_r)
        value = int(f"{f}{l}")
        print(line, words, f, l, value)
        values.append(value)

    print(values)
    print(sum(values))


if __name__ == "__main__":
    main("input.txt")
