from hashlib import sha256
import random
import numpy as np

random.seed(0)


def digBlock(probability):
    return random.random() > (1.0 - probability)


def digNBlocks(n, success_rate):
    tries = 0
    blocks = 0
    while blocks < n:
        tries += 1
        blocks += digBlock(success_rate)
    return tries


def experiment(n, q, samples):
    assert q < 0.5, f"0 < q < 0.5"
    p = 1 - q
    adversary_success = 0
    for _ in range(samples):
        userTries = digNBlocks(n, p)
        adversaryTries = digNBlocks(n, q)
        if adversaryTries <= userTries:
            adversary_success += 1
    return adversary_success / samples


if __name__ == "__main__":
    samples = 1000
    ns = [1, 3, 6, 12, 24, 48]
    for i, n in enumerate(ns):
        print(f"n={n}")
        fname = f"{i}_n_{n}_samples_{samples}.csv"
        with open(fname, 'w') as file:
            for q in np.linspace(0.01, 0.49, 49):
                q = round(q, 2)
                print(f"\tq={q}", end="\t", flush=True)
                rate = experiment(n, q, samples)
                print(f"Adversary success rate: {rate * 100:.2f}%")
                file.write(f"{q},{rate}\n")
