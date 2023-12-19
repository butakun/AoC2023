import logging
logging.basicConfig(level=logging.INFO)
from copy import deepcopy


def read(filename):
    workflows = {}
    f = open(filename)
    for l in f:
        if not l.strip():
            break
        name, workflow = l.split("{")
        workflow = workflow.strip("}\n")
        rules_ = workflow.split(",")
        rules = []
        for rule in rules_:
            tokens = rule.split(":")
            if len(tokens) == 2:
                attr = tokens[0][0]
                pred = tokens[0][1]
                value = int(tokens[0][2:])
                dest = tokens[1]
                if pred == "<":
                    r = [0, value-1]
                elif pred == ">":
                    r = [value+1, 4000]
                else:
                    raise ValueError(pred)
                rule = { "dest": dest, "attr": attr, "range": r }
            elif len(tokens) == 1:
                dest = tokens[0]
                rule = {"dest": dest}
            else:
                raise ValueError
            rules.append(rule)
        workflows[name] = rules

    return workflows


def intersection(r1, r2):
    s1 = max(r1[0], r2[0])
    s2 = min(r1[1], r2[1])
    if s1 < s2:
        return [s1, s2]
    else:
        return None


def apply_rule(rule, ranges):
    logging.debug(f"applying {rule} to {ranges}")
    next_key= None
    passed = None
    others = []
    if "attr" in rule:
        attr = rule["attr"]
        vmin, vmax = rule["range"]
        new_range = intersection((vmin, vmax), ranges[attr])
        if new_range is None:
            others.append(deepcopy(ranges))
        else:
            logging.debug(f"  intersects?: {ranges[attr]}, {new_range}")
            if ranges[attr][0] < new_range[0]:
                other = deepcopy(ranges)
                other[attr][1] = new_range[0] - 1
                others.append(other)
            if new_range[1] < ranges[attr][1]:
                other = deepcopy(ranges)
                other[attr][0] = new_range[1] + 1
                others.append(other)

            ranges[attr] = new_range
            passed = deepcopy(ranges)
            next_key = rule["dest"]

    else:
        next_key = rule["dest"]
        passed = deepcopy(ranges)

    return next_key, passed, others


def accepts(entry, ranges_start, workflows):

    accepted = []
    queue = [(ranges_start, entry, 0)]
    while queue:
        ranges, name, index = queue.pop(0)
        if name == "A":
            accepted.append(ranges)
            continue
        elif name == "R":
            continue

        rule = workflows[name][index]
        next_name, passed, others = apply_rule(rule, ranges)
        logging.debug(f"  passed {passed is not None}, and {len(others)} remaining ranges")
        queue.append((passed, next_name, 0))
        for other in others:
            queue.append((other, name, index+1))
        logging.debug(f"queue: {queue}")

    return accepted


def main(filename):
    workflows = read(filename)

    start = {"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]}
    accepted = accepts("in", start, workflows)
    print("accepted ranges = ")
    total = 0
    for a in accepted:
        multiple = 1
        for _, r in a.items():
            multiple *= (r[1] - r[0] + 1)
        print(a, multiple)
        total += multiple
    print(total)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
