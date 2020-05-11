from main import experiment
import numpy as np


def binary_search_n(upper_bound, q):
    """
    Finds the smallest `n` that provides sufficient security of success `upper_bound`
    when adversary has `q = 1 - p` computational power (0 < q < 0.5).
    """
    samples = 1000
    epsilon = 0.001
    low = 1
    high = low

    while True:
        rate = experiment(high, q, samples)
        print(f"\tn={high} | rate={rate:.4f}")
        if rate < upper_bound:
            break
        low = high
        high += high

    while high >= low:
        mid = low + ((high - low) // 2)
        rate = experiment(mid, q, samples)

        diff_rate = upper_bound - rate
        absolute_error = abs(diff_rate)

        print(f"\tn={mid} | rate={rate:.3f} | err={absolute_error:.4f}")

        if rate < upper_bound:
            high = mid - 1
        else:
            if absolute_error < epsilon:
                return mid
            low = mid + 1

    return low


if __name__ == "__main__":
    upper_bounds = [0.001, 0.01, 0.1]
    for i, upper_bound in enumerate(upper_bounds):
        print(f"upper_bound={upper_bound}")
        fname = f"{i}_upper_bound_{upper_bound}.csv"
        with open(fname, 'w') as file:
            for q in np.linspace(0.01, 0.49, 49):
                q = round(q, 2)
                n = binary_search_n(upper_bound, q)
                print(f"\t\tq={q} | n={n}")
                file.write(f"{q},{n}\n")
