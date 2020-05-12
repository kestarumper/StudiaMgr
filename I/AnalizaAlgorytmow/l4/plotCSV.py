from math import exp, factorial, comb
from pathlib import Path
import argparse
import csv
import matplotlib.pyplot as plt
import numpy as np
import re


def nakamoto(n, q):
    result = 1
    p = 1 - q
    lambd = n * (q / p)
    for k in range(n):
        result -= exp(-lambd) * ((lambd ** k) / factorial(k)) * \
            (1 - ((q / p) ** (n - k)))
    return result


def grunspan(n, q):
    result = 1
    p = 1 - q
    for k in range(n):
        result -= ((p ** n) * (q ** k) - (q ** n)
                   * (p ** k)) * comb(k + n - 1, k)
    return result


def plot_nakamoto_and_grunspan(n):
    xs = []
    ys = []
    yss = []
    for q in np.linspace(0.01, 0.49, 49):
        q = round(q, 2)
        P = nakamoto(n, q)
        P2 = grunspan(n, q)
        xs.append(q)
        ys.append(P)
        yss.append(P2)
    plt.plot(xs, ys, c="blue", label="nakamoto")
    plt.plot(xs, yss, c="green", label="grunspan")
    return xs, ys


def main():
    parser = argparse.ArgumentParser(description='Plotter.')
    parser.add_argument("-t", "--title",
                        help="Title")
    parser.add_argument("--log-scale", help="Set logarithmic scale", action='store_true')
    parser.add_argument("-x", "--xlabel", default="q",
                        help="Arguments label")
    parser.add_argument("-y", "--ylabel", default="adversary success rate",
                        help="Values label")
    parser.add_argument("-f", "--file",
                        help="File to be processed")
    args = parser.parse_args()

    xlabel = args.xlabel
    ylabel = args.ylabel
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

        ymax = max(y)
        if ymax <= 1:
            plt.annotate(f"{ymax * 100:.2f}%", xy=(
                x[-1], y[-1]), xytext=(-25, 10), textcoords='offset points', va='center')

        if args.log_scale:
            plt.yscale('log')

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.plot(x, y, c="red", label="experiment")

        n = re.search("n_(\d+)_", Path(args.file).stem)
        if n:
            n = int(n.group(1))
            plot_nakamoto_and_grunspan(n)

        plt.legend()
        plt.savefig(f"{Path(args.file).stem}.png")


if __name__ == "__main__":
    main()
