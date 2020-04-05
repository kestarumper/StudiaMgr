import numpy as np
import hashlib
import string
import random
import argparse
import math


def p(num):
    result = num.find('1')
    if result == -1:
        return 33
    return result + 1


def getAlpha(m):
    a = {
        16: 0.673,
        32: 0.697,
        64: 0.709
    }
    return a.get(m, 0.7213 / (1 + 1.079 / m))


def hyper_log_log(multiset, h, m, b):
    M = [0] * m
    for v in multiset:
        x = h(v)
        x_1 = x[:b]
        j = int(x_1, 2)
        w = x[b:]
        assert len(x_1) + len(w) == 32
        M[j] = max(M[j], p(w))

    a_m = getAlpha(m)
    E = a_m * (m ** 2) * (
        1 / sum(map(lambda M_j: 0.5 ** M_j, M))
    )

    if E < 5/2 * m:
        V = len(list(filter(lambda x: x == 0, M)))
        if V != 0:
            return m * math.log(m / V)
        else:
            return E
    if E <= 1/30 * (2 ** 32):
        return E
    if E > 1/30 * (2 ** 32):
        return -(2 ** 32) * math.log(1 - E / (2 ** 32))

    raise Exception("Did not return any value!")

def max_bin_val(length):
    return float(int('1' * length, 2))


def hash_fn_factory(name):
    def Fn(data):
        hasher = hashlib.new(name, data)
        hash = hasher.hexdigest()[:8]
        value = int(hash, 16)
        return format(value, f"032b")
    return Fn


def main():
    parser = argparse.ArgumentParser(description='HyperLogLog.')
    parser.add_argument("-n", "--number", type=int,
                        help="How many elements", default=10000)
    parser.add_argument("-b", type=int,
                        help="Parameter b.", required=True,
                        choices=list(range(4, 17)))
    parser.add_argument("-f", required=True,
                        choices=hashlib.algorithms_available,
                        help="Hash function")

    test_val = "00010000000000000000000011111111"
    assert p(test_val) == 4
    test_val = "10010000000000000000000011111111"
    assert p(test_val) == 1
    test_val = "00000000000000000000000000000000"
    assert p(test_val) == 33

    args = parser.parse_args()
    np.random.seed(0)

    b = args.b
    m = 2 ** b
    h = hash_fn_factory(args.f)

    successes = 0
    with open(f"hll_{args.f}_n_{args.number}_b_{b}_m_{m}.csv", 'w') as out_file:
        for nAll in range(1, args.number + 1):
            multiset = np.random.randint(0, nAll, size=nAll)
            n = np.unique(multiset).size

            result = hyper_log_log(multiset, h, m, b)
            ratio = result / float(n)

            if abs(ratio - 1.0) < 0.1:
                successes += 1

            if not nAll % 100:
                err = abs(ratio - 1)*100
                print(f"{nAll}\t|n={n}\t| n̂={result}\t| err={err:.2f}%")
            out_file.write(f"{n},{result},{ratio}\n")

    success_rate = successes / float(args.number)
    print(f"b = {b}\t| Precision (-10% < x < +10%): {success_rate}")

    


if __name__ == "__main__":
    main()
