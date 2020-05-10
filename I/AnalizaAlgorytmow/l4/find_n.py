from main import experiment
import numpy as np


def find_n(upper_bound, q):
    samples = 1000
    n = 24
    epsilon_rate = 0.001
    max_iterations = 15

    best_n = n
    best_err = 1
    for i in range(max_iterations):
        rate = experiment(n, q, samples)
        print(f"\tn={n} | rate={rate}")

        diff_n = n // 2
        diff_rate = upper_bound - rate
        absolute_error = abs(diff_rate)

        if absolute_error < best_err:
            best_n = n
            best_err = absolute_error

        if (diff_n == 0) or (absolute_error < epsilon_rate):
            print(f"\t\tINFO:\tFound after {i} iterations.")
            return n
        if diff_rate > 0:
            n -= diff_n
        else:
            n += diff_n
        
    print(f"\t\tWARN:Max iterations exceeded.")
    return best_n


if __name__ == "__main__":
    upper_bounds = [0.001, 0.01, 0.1]
    for i, upper_bound in enumerate(upper_bounds):
        print(f"upper_bound={upper_bound}")
        fname = f"{i}_upper_bound_{upper_bound}.csv"
        with open(fname, 'w') as file:
            for q in np.linspace(0.01, 0.49, 49):
                q = round(q, 2)
                n = find_n(upper_bound, q)
                print(f"\t\tq={q} | n={n}")
                file.write(f"{q},{n}\n")
