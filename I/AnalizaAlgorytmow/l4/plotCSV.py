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
    with open(args.file, "r", newline='') as csvfile:
        data = list(csv.reader(csvfile))
        x = []
        y = []
        for d in data:
            q, rate = d
            x.append(float(q))
            y.append(float(rate))
        plt.title(title)
        # plt.ylim(0.0, 0.8)
        plt.xlabel("q")
        plt.ylabel("adversary success rate")
        plt.annotate(f"{max(y) * 100:.2f}%", xy=(
            x[-1], y[-1]), xytext=(-25, 10), textcoords='offset points', va='center')
        plt.plot(x, y, c="red")
        plt.savefig(f"{Path(args.file).stem}.png")


if __name__ == "__main__":
    main()
