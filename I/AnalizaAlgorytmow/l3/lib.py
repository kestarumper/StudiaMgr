import math
import hashlib
from struct import unpack
from functools import reduce
from itertools import count


def concat_bits(i, k):
    return f"{i:b}{k:b}"


def hash_fn_factory(name, length):
    max_val = 2**(length * 8)

    def Fn(data):
        hash = hashlib.new(name, data.encode('utf-8'))
        return float(unpack('L', hash.digest()[:length])[0]) / max_val

    return Fn


def unique_sum(multiset, h, m):
    M = [math.inf] * m
    for s in multiset:
        (i, yi) = s
        for k in range(m):
            u = h(concat_bits(i, k))
            M[k] = min(M[k], -math.log(u) / yi)
    return (m - 1) / sum(M)


__infinite_sequence = count(0, 1)


def uuid():
    return next(__infinite_sequence)


def generate_dataset(n, get_val):
    multiset = [(uuid(), get_val()) for i in range(n)]
    expected_sum = 0
    for (_, v) in multiset:
        expected_sum += v
    return multiset, expected_sum


def get_rate(expected, approx):
    return approx / expected


def run_tests():
    assert concat_bits(2, 1) == '101'

    n = 1000
    m = 2**6
    multiset, expected = generate_dataset(n, lambda: 1)
    h = hash_fn_factory('sha3_256', 8)

    approx = unique_sum(multiset, h, m)
    rate = get_rate(expected, approx)
    print(expected, approx, rate, f"err={abs((1 - rate)*100):.2f}%")
    print(multiset)


if __name__ == "__main__":
    run_tests()
