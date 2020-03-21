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
    print(M)
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
    return np.random.choice(list(string.ascii_lowercase),  size=length)


def main():
    multiset = rand_str(100000)
    h = hash_fn_factory('md5')
    k = 3
    result = min_count(multiset, h, k)
    print(result)


if __name__ == "__main__":
    main()
    pass
