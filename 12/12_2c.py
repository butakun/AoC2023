import logging
logging.basicConfig(level=logging.WARNING)
#logging.basicConfig(level=logging.DEBUG)
import numpy as np
import sys
import itertools


def read(filename):
    lines = [l.strip().split() for l in open(filename)]
    records = [ [ l[0].strip(), [int(i) for i in l[1].split(",")] ] for l in lines]
    return records


def multiply(records, a=5):
    return [ ["?".join([pattern] * a), strips * a] for pattern, strips in records ]


def look(matching, pattern, strips, context):
    """ matching: int, number of chars of "#" that have been matched
    patter: the string patter,
    strips: list of "#"-strip lengths
    returns: the number of ways it can match"""

    h = (matching, pattern, tuple(strips))
    if h in context:
        return context[h]

    logging.debug(f"{matching}, '{pattern}', {strips}")

    if strips:
        if pattern:  # "###", "****", [3, 2, 1]
            c = pattern[0]
            if c == ".":
                if strips[0] == matching:
                    #print(f".->. match, consuming {strips[0]}")
                    count = look(0, pattern[1:], strips[1:], context)
                    context[h] = count
                    return count
                if matching == 0:
                    count = look(0, pattern[1:], strips, context)
                    context[h] = count
                    return count
                else:
                    context[h] = 0
                    return 0
            elif c == "#":
                if strips[0] > matching:
                    count = look(matching + 1, pattern[1:], strips, context)
                    context[h] = count
                    return count
                else:
                    context[h] = 0
                    return 0
            elif c == "?":
                # ? -> #
                if strips[0] > matching:
                    count1 = look(matching + 1, pattern[1:], strips, context)
                else:
                    count1 = 0

                # ? -> .
                if strips[0] == matching:
                    #print(f"?-. match, consuming {strips[0]}")
                    count2 = look(0, pattern[1:], strips[1:], context)
                elif matching == 0:
                    count2 = look(0, pattern[1:], strips, context)
                else:
                    count2 = 0
                count = count1 + count2
                context[h] = count
                return count
        else:
            # pattern "", strips [3, 2, 1]
            if matching == strips[0]:
                count = look(0, pattern, strips[1:], context)
                context[h] = count
                return count
            elif matching < strips[0]:
                context[h] = 0
                return 0
            else:
                assert False, "should not be here"
    else:
        if pattern:
            c = pattern[0]
            if c == ".":
                count = look(matching, pattern[1:], strips, context)
            elif c == "?":
                count = look(matching, pattern[1:], strips, context)
            elif c == "#":
                count = 0
        else:
            # pattern "", strips []
            logging.debug("all matched")
            count = 1
        context[h] = count
        return count


def main(filename):
    records = read(filename)
    records = multiply(records, 5)

    count = 0
    for pattern, strips in records:
        context = {}
        ways = look(0, pattern, strips, context)
        logging.warning(f"{ways} ways")
        count += ways
    print(count)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
