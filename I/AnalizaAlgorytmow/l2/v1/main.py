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
        hasher = hashlib.new(name, data.to_bytes(8, 'big', signed=True))
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

    ks = [args.hashes] if args.hashes else [2, 3, 10, 100, 400]
    h = hash_fn_factory(args.function)

    for k in ks:
        successes = 0
        with open(f"{args.function}_{k}.csv", 'w') as out_file:
            for n in range(1, args.number + 1):
                # multiset = np.random.randint(n, size=n)
                multiset = range(n)
                result = min_count(multiset, h, k)
                if abs((result / float(n)) - 1) < 0.1:
                    successes += 1
                if not n % 100:
                    print(f"n={len(multiset)}\t| n̂={result}")
                out_file.write(f"{len(multiset)},{result}\n")
        success_rate = successes / float(n)
        print(f"k = {k}\t| Success rate of error rate +-10%: {success_rate}")


if __name__ == "__main__":
    main()
