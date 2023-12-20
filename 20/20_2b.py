import logging
logging.basicConfig(level=logging.INFO)
import numpy as np


def read(filename):
    circuit = {}
    for l in open(filename):
        if l[0] == "#":
            continue
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


def reset_circuit(circuit):
    for name, node in circuit.items():
        _, kind, _, _ = node
        if kind == "F":
            node[2] = False
        elif kind == "C":
            for k in node[2]:
                node[2][k] = False


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


def button(circuit, capture):
    queue = [(False, "button", "broadcaster")]

    captured = []
    highs, lows = 0, 1
    while queue:
        signal, src, dest = queue.pop(0)
        out = process(circuit[dest], src, signal)
        logging.debug(f"signal {signal}, src {src}, dest {dest} ({circuit[dest][2]}) -> out = {out}")

        if not out:
            continue

        for s, _, d in out:
            if d == "rx" and s == False:
                assert False
                return True

        if dest == capture:
            assert len(out) == 1
            if out[0][0]:
                captured.append(True)

        values = [ o[0] for o in out ]
        high_count = sum(values)
        low_count = len(values) - high_count
        highs += high_count
        lows += low_count
        queue.extend(out)
    return False, captured


def conj(p):
    state = p[2]
    ss = [ 1 if s else 0 for s in state.values() ]
    buf = " ".join([f"{k}:{1 if v else 0}" for k, v in state.items()])
    su = sum(ss)
    return buf + f":{su}", su


def condense_state(p):
    state = p[2]
    ss = tuple( 1 if s else 0 for s in state.values() )
    return ss


def circuit_state(circuit):
    signature = []
    for node, (_, kind, state, _) in circuit.items():
        if state is None:
            continue
        if isinstance(state, list):
            signature += state
        elif isinstance(state, dict):
            signature += [v for v in state.values()]
        else:
            signature += [state]
    signature = tuple(signature)
    s = "".join([f"{int(v)}" for v in signature])
    return signature, s


def dot(circuit, f):
    print("digraph {", file=f)
    for node, (_, kind, _, dests) in circuit.items():
        if kind == "F":
            shape = "box"
        elif kind == "C":
            shape = "circle"
        elif kind == "B":
            shape = "diamond"
        else:
            shape = "plaintext"
        print(f"{node} [shape={shape}];", file=f)
        if dests:
            print(f"{node} -> {{ {' '.join(dests)} }};", file=f)
    print("}", file=f)


def monitor(circuit, capture):

    sig = circuit_state(circuit)
    history = [sig]

    period = None
    highs = []
    for i in range(1000000):
        on, captured = button(circuit, capture=capture)

        if any(captured):
            highs.append(i+1)
            print(f"*** {i+1}: {capture} high {captured}")
            if len(highs) == 2:
                print(f"exiting highs occurred at {highs}")
                assert highs[1] == highs[0] * 2
                break

        sig, s = circuit_state(circuit)

        s = "".join([f"{int(v)}" for v in sig])
        logging.info(f"{i+1}: captured = {captured}, sig = {s}")

        if period is None:
            if sig in history:
                i0 = history.index(sig)
                period = i + 1 - i0
                print(f"{i+1}: repeated state at {i0}, {s}, {highs}, period = {period}")
                break
        else:
            if  ((i + 1) // period) == 2:
                print(f"{i+1}: repeated state at {i0}, {s}, {highs}, period = {period}")
                break
        history.append(sig)

    return highs[0]


def main(filename):
    circuit = read(filename)
    print(circuit)
    #dot(circuit, open("dot", "w"))
    #return

    captures = ["tx", "ph", "dd", "nz"]
    periods = {}

    for capture in captures:
        reset_circuit(circuit)
        i = monitor(circuit, capture)
        periods[capture] = i

    print(periods)

    pp = [v for v in periods.values()]
    lcm = np.lcm.reduce(pp)
    print(lcm)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
