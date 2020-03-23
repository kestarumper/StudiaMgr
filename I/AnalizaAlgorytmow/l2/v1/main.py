import numpy as np
import hashlib
import string
import random


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
        hasher = hashlib.new(name, data.encode('utf-8'))
        max_val = float(int('ff' * hasher.digest_size, 16))
        return int(hasher.hexdigest(), 16) / max_val
    return Fn


def rand_str(length):
    return np.random.choice(list(string.ascii_lowercase), size=length)


def main():
    multisets = [rand_str(n) for n in range(1, 10001)]
    ks = [2, 3, 10, 100, 400]
    h = hash_fn_factory('md5')

    for multiset in multisets:
        for k in ks:
            result = min_count(multiset, h, k)
            print(f"n={len(multiset)}\t|\tk={k}\t|\test={result}")


if __name__ == "__main__":
    main()
    pass
