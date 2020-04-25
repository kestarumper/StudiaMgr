import csv
import argparse
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Plotter.')
    parser.add_argument("-t", "--title",
                        help="Title")
    parser.add_argument("-f", "--file",
                        help="File to be processed")
    args = parser.parse_args()

    title = args.title
    if not title:
        title = args.file

    print(f"Processing {args.file}...")
    with open(args.file, newline='') as csvfile:
        data = list(csv.reader(csvfile))
        x = []
        y = []
        for d in data:
            n, _, ratio = d
            x.append(int(n))
            y.append(float(ratio))
        plt.ylim(0.5, 2.0)
        plt.title(title)
        plt.xlabel("n")
        plt.ylabel("sum'/sum")
        plt.scatter(x, y, s=1, c="red")
        plt.savefig(f"{Path(args.file).stem}.png")


if __name__ == "__main__":
    main()
