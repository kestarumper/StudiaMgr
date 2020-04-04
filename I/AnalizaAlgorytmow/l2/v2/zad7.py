import csv
import argparse
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, log
from pathlib import Path


def getDeltaChebychew(n, k, alpha):
    return sqrt(
        (n - k + 1) / (n * alpha * (k - 2))
    )


def getDeltaChernoff(n, alpha):
    return sqrt(
        3 * log(2 / alpha) / n
    )


def main():
    parser = argparse.ArgumentParser(description='MinCount.')
    parser.add_argument("-a", "--alpha", type=float, help="Alpha parameter")
    parser.add_argument("-f", "--file", help="Input file")
    args = parser.parse_args()

    k = 400
    alpha = args.alpha

    with open(args.file, newline='') as csvfile:
        data = list(csv.reader(csvfile))
        x = []
        y = []
        y_chebyshew_upper = []
        y_chebyshew_lower = []
        y_chernoff_upper = []
        y_chernoff_lower = []

        delta_chebyshew = getDeltaChebychew(10000, k, alpha)
        delta_chernoff = getDeltaChernoff(10000, alpha)

        for d in data:
            n, approx, _ = d
            n = int(n)
            approx = float(approx)

            x.append(n)
            y.append(approx)

            y_chebyshew_upper.append(n + n * delta_chebyshew)
            y_chebyshew_lower.append(n - n * delta_chebyshew)

            y_chernoff_upper.append(n + n * delta_chernoff)
            y_chernoff_lower.append(n - n * delta_chernoff)

        plt.scatter(x, y, s=0.1)
        plt.scatter(x, y_chebyshew_upper, color="C1", label="Chebyshew", s=0.1)
        plt.scatter(x, y_chebyshew_lower, color="C1", s=0.1)
        plt.scatter(x, y_chernoff_upper, color="C2", label="Chernoff", s=0.1)
        plt.scatter(x, y_chernoff_lower, color="C2", s=0.1)
        plt.legend()
        plt.title(f"{Path(args.file).stem} α = {alpha}")
        plt.savefig(f"{Path(args.file).stem}_α_{alpha}_k_{k}_n_{10000}.png")


if __name__ == "__main__":
    main()
