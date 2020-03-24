import csv
import argparse
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='MinCount.')
    parser.add_argument("-f", "--file",
                        help="How many hashes")
    args = parser.parse_args()

    with open(args.file, newline='') as csvfile:
        data = list(csv.reader(csvfile))
        x = []
        y = []
        for i, d in enumerate(data):
            if i % 25:
                continue
            n, approx = d
            n_hat = float(approx) / int(n)
            x.append(int(n))
            y.append(n_hat)

        plt.plot(x, y)
        plt.savefig(f"{Path(args.file).stem}.png")


if __name__ == "__main__":
    main()
