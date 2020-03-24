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
    parser.add_argument("-k", "--hashes", type=int,
                        help="How many hashes")

    args = parser.parse_args()

    ks = [args.hashes] if args.hashes else [2, 3, 10, 100, 400]
    # ks = [args.hashes]
    h = hash_fn_factory('md5')

    for k in ks:
        with open(f"result_{k}.csv", 'w') as out_file:
            for n in range(1, 10001):
                # multiset = np.random.randint(n, size=n)
                multiset = range(n)
                result = min_count(multiset, h, k)
                print(f"n={len(multiset)}\t|\test={result}")
                out_file.write(f"{len(multiset)},{result}\n")


if __name__ == "__main__":
    main()
