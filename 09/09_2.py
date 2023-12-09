import numpy as np


def read(filename):
    sequences = [ [int(v) for v in l.strip().split()] for l in open(filename) ]
    return sequences


def naive(start):

    seqs = [np.array(start, dtype=int)]

    s = seqs[-1]
    while not np.all(s == 0):
        s0 = seqs[-1]
        s = s0[1:] - s[:-1]
        seqs.append(s)

    print(seqs)

    seqs[-1] = np.concatenate([np.array([0]), seqs[-1]])

    L = len(seqs)
    for i in range(1, L):
        seq1 = seqs[L - i - 1]
        seq2 = seqs[L - i]
        prev_value = seq1[0] - seq2[0]
        seq1 = np.concatenate([np.array([prev_value]), seq1])
        seqs[L - i - 1] = seq1
    print(seqs)
    return seqs[0][0]

def main(filename):
    sequences = read(filename)
    print(sequences)

    sum = 0
    for s in sequences:
        sum += naive(s)
    print(sum)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
