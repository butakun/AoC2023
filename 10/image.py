import argparse
import numpy as np
import cv2
from pathlib import Path


def main(filename, marker, scale):
    with open(filename) as f:
        pond = [list(l.strip()) for l in f]
        pond = np.array(pond)

    frame = np.zeros(pond.shape, dtype=np.uint8)
    for i in range(pond.shape[0]):
        for j in range(pond.shape[1]):
            p = pond[i, j]
            if p == "P":
                frame[i, j] = 255
            elif p == marker:
                frame[i, j] = 127

    dsize = int(frame.shape[1] * scale), int(frame.shape[0] * scale)
    scaled = cv2.resize(frame, dsize)
    outname = Path(filename).with_suffix(".png")
    cv2.imwrite(outname.as_posix(), scaled)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="big_pond.txt")
    parser.add_argument("--marker", default="-")
    parser.add_argument("--scale", type=float, default=2.0)
    args = parser.parse_args()
    main(args.filename, args.marker, args.scale)
