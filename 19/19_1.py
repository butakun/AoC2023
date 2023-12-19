import logging
logging.basicConfig(level=logging.INFO)


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
                    logging.debug(f"  pred = {pred}, value = '{value}'")
                    func = lambda p, a=attr, v=value: p[a] < v
                elif pred == ">":
                    logging.debug(f"  pred = {pred}, value = '{value}'")
                    func = lambda p, a=attr, v=value: p[a] > v
                else:
                    raise ValueError(pred)
                rule = {"func": func, "dest": dest}
            elif len(tokens) == 1:
                dest = tokens[0]
                rule = {"dest": dest}
            else:
                raise ValueError
            rules.append(rule)
        workflows[name] = rules

    parts = []
    for l in f:
        part = {}
        l = l.strip("{}\n")
        tokens = l.split(",")
        for t in tokens:
            attr, val = t.split("=")
            assert attr in "xmas"
            part[attr] = int(val)
        parts.append(part)

    return workflows, parts


def process(part, workflows):
    rules = workflows["in"]
    while True:
        logging.debug(f"testing rules: {rules}")
        for rule in rules:
            dest = rule["dest"]
            if "func" not in rule:
                if dest == "R" or dest == "A":
                    return dest == "A"
                rules = workflows[dest]
                logging.debug(f"  go to {dest}")
                break
            f = rule["func"]
            res = f(part)
            logging.debug(f"  func result = {res}")
            if f(part):
                if dest == "R" or dest == "A":
                    return dest == "A"
                rules = workflows[dest]
                logging.debug(f"  go to {dest}")
                break
    assert False


def main(filename):
    workflows, parts = read(filename)

    total = 0
    for part in parts:
        logging.debug(f"{part}")
        accept = process(part, workflows)
        if accept:
            v = part["x"] + part["m"] + part["a"] + part["s"]
            total += v
            logging.debug(f"  ACCEPT: {v}")
        else:
            logging.debug("  REJECT")
    print(total)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
