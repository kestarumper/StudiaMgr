from lib import generate_dataset, hash_fn_factory, unique_mean, get_rate
import hashlib
import argparse
from time import sleep
import sys
import random
import time


random.seed(0)


def progress_bar(current, max):
    i = int(current / max * 20)
    sys.stdout.write('\r')
    # the exact output you're looking for:
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()


def experiment(n, m, fn_name, get_val):
    multiset, expected = generate_dataset(n, get_val)
    h = hash_fn_factory(fn_name, 8)

    approx = unique_mean(multiset, h, m)
    expected_mean = expected / n
    rate = get_rate(expected_mean, approx)
    return approx, rate


MAX_N = 1000


def strategy_uniform_a_b(a, b):
    return lambda: random.uniform(a, b)


def main():
    parser = argparse.ArgumentParser(description='MinCount.')
    parser.add_argument("-m", "--registers", type=int,
                        help="How many registers", required=True)
    parser.add_argument("-f", "--function", default="md5", required=True,
                        choices=hashlib.algorithms_available,
                        help="Hash function")

    args = parser.parse_args()
    m = args.registers
    fn_name = args.function

    strategies = [
        ("uniform_1_1000", strategy_uniform_a_b(1, MAX_N)),
    ]

    for (name, strategy) in strategies:
        print(f"Strategy: {name}")
        start = time.time()
        with open(f"mean_{name}_{fn_name}_{m}.csv", 'w') as out_file:
            for n in range(1, MAX_N + 1):
                approx, rate = experiment(n, m, fn_name, strategy)
                if not n % 10:
                    progress_bar(n, MAX_N)
                out_file.write(f"{n},{approx},{rate}\n")
        end = time.time()
        print(f"\nduration: {end - start}sec")


if __name__ == "__main__":
    main()
