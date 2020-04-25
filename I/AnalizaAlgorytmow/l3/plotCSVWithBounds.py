import csv
import argparse
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from math import sqrt


def getDeltaChebychew(m, alpha):
    return sqrt(
        1 / (alpha * (m - 2))
    )


def main():
    parser = argparse.ArgumentParser(description='Plotter.')
    parser.add_argument("-t", "--title",
                        help="Title")
    parser.add_argument("-a", "--alpha", type=float,
                        help="Alpha parameter", required=True)
    parser.add_argument("-m", "--registers", type=int,
                        help="How many registers", required=True)
    parser.add_argument("-f", "--file",
                        help="File to be processed")
    args = parser.parse_args()

    title = args.title
    if not title:
        title = args.file

    alpha = args.alpha
    m = args.registers

    print(f"Processing {args.file}...")
    with open(args.file, newline='') as csvfile:
        data = list(csv.reader(csvfile))
        x = []
        y = []
        y_chebyshew_upper = []
        y_chebyshew_lower = []

        delta_chebyshew = getDeltaChebychew(m, alpha)

        for d in data:
            n, _, ratio = d
            x.append(int(n))
            y.append(float(ratio))

            y_chebyshew_upper.append(1+delta_chebyshew)
            y_chebyshew_lower.append(1-delta_chebyshew)

        plt.ylim(min(0.5, min(y), min(y_chebyshew_lower)),
                 max(2.0, max(y), max(y_chebyshew_upper)))
        plt.title(f"{title} α={alpha}")
        plt.xlabel("n")
        plt.ylabel("sum'/sum")

        plt.scatter(x, y_chebyshew_upper, color="C1", label="Chebyshew", s=1)
        plt.scatter(x, y_chebyshew_lower, color="C1", s=1)

        plt.scatter(x, y, s=1, c="red")
        plt.savefig(f"{Path(args.file).stem}_m_{m}_a_{alpha}.png")


if __name__ == "__main__":
    main()
