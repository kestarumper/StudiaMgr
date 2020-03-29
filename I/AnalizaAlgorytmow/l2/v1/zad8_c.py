import csv
import argparse
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def get_mean_error(data):
    sum_err = 0
    for d in data:
        n, approx, ratio = d
        n = int(n)
        approx = float(approx)
        ratio = float(ratio)
        err = abs(ratio - 1)
        sum_err += err
    return sum_err / len(data)


def main():
    parser = argparse.ArgumentParser(description='MinCount.')
    parser.add_argument("-f1")
    parser.add_argument("-f2")
    args = parser.parse_args()

    f1 = args.f1
    f2 = args.f2

    f1_err = 0
    with open(f1, newline='') as csvfile:
        data = list(csv.reader(csvfile))
        f1_err = get_mean_error(data)

    f2_err = 0
    with open(f2, newline='') as csvfile:
        data = list(csv.reader(csvfile))
        f2_err = get_mean_error(data)

    print(f"{f1} err = {f1_err*100:.2f}%")
    print(f"{f2} err = {f2_err*100:.2f}%")


if __name__ == "__main__":
    main()
