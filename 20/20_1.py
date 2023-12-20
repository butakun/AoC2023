import logging
logging.basicConfig(level=logging.INFO)


class FlipFlop:
    def __init__(self, name):
        self.name = name
        self.state = False
        self.queue = []
    def __call__(self, sig):
        if sig:
            return
        else:
            self.state = not self.state
            if self.state:
                pass
            else:
                pass

    def register_input(self, inp):
        pass


class Conjunction:
    def __init__(self, name):
        self.name = name
        self.inputs = {}
    def register_input(self, inp):
        self.inputs[inp] = False

def read(filename):
    circuit = {}
    for l in open(filename):
        src, dests = l.strip().split(" -> ")
        dests = [d.strip() for d in dests.split(",")]
        if src[0] == "%":
            name = src[1:]
            kind = "F"
            state = False
        elif src[0] == "&":
            name = src[1:]
            kind = "C"
            state = {}
        elif src == "broadcaster":
            name = src
            kind = "B"
            state = False
        else:
            assert False

        circuit[name] = [name, kind, state, dests]

    untyped = []
    for src, part in circuit.items():
        dests = part[3]
        for d in dests:
            if d not in circuit:
                untyped.append(d)
                continue
            dest = circuit[d]
            if dest[1] == "C":
                dest[2][src] = False

    for d in untyped:
        if d not in circuit:
            circuit[d] = [d, None, None, None]

    return circuit


def process(part, src, signal):
    name, kind, state, dests = part
    if kind == "F":
        if signal == 1:
            return None
        part[2] = not part[2]
        o = True if part[2] else False
        out = [(o, name, d) for d in dests]
        return out
    elif kind == "C":
        state[src] = signal
        if all(state.values()):
            out = [(False, name, d) for d in dests]
            return out
        else:
            out = [(True, name, d) for d in dests]
            return out
    elif kind == "B":
        out = [(signal, name, d) for d in dests]
        return out
    elif kind is None:
        pass
    else:
        raise ValueError(kind)


def button(circuit):
    queue = [(False, "button", "broadcaster")]

    highs, lows = 0, 1
    while queue:
        signal, src, dest = queue.pop(0)
        out = process(circuit[dest], src, signal)
        logging.debug(f"out = {out}")

        if not out:
            continue

        values = [ o[0] for o in out ]
        high_count = sum(values)
        low_count = len(values) - high_count
        logging.debug(f"H: {high_count}, L: {low_count}")
        highs += high_count
        lows += low_count
        queue.extend(out)
    return highs, lows


def main(filename):
    circuit = read(filename)
    print(circuit)

    hh, ll = 0, 0
    for i in range(1000):
        highs, lows = button(circuit)
        print(f"{i}: H = {highs}, L = {lows}")
        hh += highs
        ll += lows
    print(hh, ll, hh * ll)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
