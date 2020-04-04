import numpy as np
import hashlib
import string
import random
import argparse


def min_count(multiset, h, k):
    M = np.empty(k)
    M.fill(1.0)
    for x in multiset:
        hash = h(x)
        if hash < M[k-1] and (hash not in M):
            M[k-1] = hash
            M = np.sort(M)
    if M[k-1] == 1.0:
        return np.where(M != 1.0, 1, 0).sum()
    return (k-1) / M[k-1]


def hash_fn_factory(name):
    def Fn(data):
        hasher = hashlib.new(name, data)
        max_val = float(int('ff' * hasher.digest_size, 16))
        return int(hasher.hexdigest(), 16) / max_val
    return Fn


def main():
    parser = argparse.ArgumentParser(description='MinCount.')
    parser.add_argument("-k", "--hashes", type=int, help="How many hashes")
    parser.add_argument("-n", "--number", type=int,
                        help="How many elements", default=10000)
    parser.add_argument("-f", "--function", default="md5", required=True,
                        choices=hashlib.algorithms_available,
                        help="Hash function")

    args = parser.parse_args()
    np.random.seed(0)

    ks = [args.hashes] if args.hashes else [2, 3, 10, 100, 400]
    h = hash_fn_factory(args.function)

    for k in ks:
        successes = 0
        with open(f"{args.function}_{k}.csv", 'w') as out_file:
            for nAll in range(1, args.number + 1):
                multiset = np.random.randint(0, nAll, size=nAll)
                n = np.unique(multiset).size

                result = min_count(multiset, h, k)
                ratio = result / float(n)

                if abs(ratio - 1.0) < 0.1:
                    successes += 1

                if not nAll % 100:
                    print(f"{nAll}\t| n={n}\t| n̂={result}\t| ratio={ratio}")
                out_file.write(f"{n},{result},{ratio}\n")

        success_rate = successes / float(args.number)
        print(f"k = {k}\t| Precision (-10% < x < +10%): {success_rate}")


if __name__ == "__main__":
    main()
