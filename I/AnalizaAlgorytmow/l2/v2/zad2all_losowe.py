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


def max_bin_val(length):
    return float(int('1' * length, 2))


def hash_fn_factory(name, length):
    max_length = hashlib.new(name).digest_size * 8
    length = min(length, max_length)

    max_val = max_bin_val(length)

    def Fn(data):
        hasher = hashlib.new(name, data)
        hash = int(hasher.hexdigest(), 16)
        hash_bin = format(hash, f"0{hasher.digest_size * 8}b")
        hash_len = len(hash_bin)
        divide_by = hash_len - length
        value = hash >> divide_by
        normalized = (value / max_val)
        # print(f"{hash_bin} (len={hash_len})")
        # print(f"{bin(value)[2:]} (len={length})")
        # print(f"{normalized}")
        return normalized
    return Fn


def main():
    parser = argparse.ArgumentParser(description='MinCount.')
    parser.add_argument("-k", type=int,
                        help="How many hashes", required=True)
    parser.add_argument("-n", type=int,
                        help="How many elements", required=True)

    args = parser.parse_args()

    k = args.k
    n = args.n

    np.random.seed(0)
    multiset = np.random.randint(0, n, size=n)
    n = np.unique(multiset).size

    bs = list(range(8, 257, 8))
    hs = ["md5", "sha1", "sha3_224", "sha256"]

    for b in bs:
        print(f"============================b={b}============================")
        for h_name in hs:
            h = hash_fn_factory(h_name, b)
            result = min_count(multiset, h, k)
            err = abs(result/n - 1)*100
            print(f"{h_name:>8} | n̂={result}\t| n={n}\t| err={err:.2f}%")


if __name__ == "__main__":
    main()
