import numpy as np
from pathlib import Path
import imageio
import cv2
import argparse


def generate_frame(bg, best):
    frame = bg.copy()
    if best is not None:
        path = best[3]
        for i, j in path:
            frame[i, j] = 255
    return frame


def main(log_filename):
    fi = open(log_filename)
    idim, jdim = None, None
    bg = None
    best = None
    istep_last = None
    frames = []
    for line in fi:
        tokens = line.strip().split(",")
        istep = int(tokens[0])
        if istep_last is None:
            istep_last = istep
        if istep != istep_last and bg is not None:
            if istep % 1000 == 0:
                print(istep)
                frame = generate_frame(bg, best)
                frames.append(frame)
            istep_last = istep
            best = None

        typ = tokens[1]
        if typ == "DIMENSIONS":
            idim = int(tokens[2])
            jdim = int(tokens[3])
            bg = np.zeros((idim, jdim), dtype=np.uint8)
        elif typ == "INSPECT":
            i, j, w = int(tokens[2]), int(tokens[3]), int(tokens[4])
            assert w >= 0 and w < 10
            xi = (9 - w) / 9
            pixel = (1.0 - xi) * 127 + xi * 255
            bg[i, j] = pixel
        elif typ == "BETTER":
            i, j, d = int(tokens[2]), int(tokens[3]), int(tokens[4])
            p = tokens[5].split(" ")
            path = [(int(i), int(j)) for i, j in zip(p[:-1:2], p[1::2])]
            if best is None:
                best = (i, j, d, path)
            elif d < best[2]:
                best = (i, j, d, path)

    if best:
        frames.append(generate_frame(bg, best))

    # resize
    a = 3
    out_path = Path(log_filename).with_suffix(".gif")
    frames = [cv2.resize(frame, (a * idim, a * jdim)) for frame in frames]
    imageio.mimwrite(out_path.as_posix(), frames)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    main(args.filename)
