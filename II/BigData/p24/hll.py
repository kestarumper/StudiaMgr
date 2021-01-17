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
        hasher = hashlib.new(name, data.encode('utf-8'))
        hash = hasher.hexdigest()[:8]
        value = int(hash, 16)
        return format(value, f"032b")
    return Fn

class HyperLogLog:
    def __init__(self, h, b):
        self.h = hash_fn_factory(h)
        self.m = 2 ** b
        self.b = b
        self.M = [0] * self.m
    
    def add(self, v):
        h = self.h
        b = self.b
        M = self.M

        x = h(v)
        x_1 = x[:b]
        j = int(x_1, 2)
        w = x[b:]
        assert len(x_1) + len(w) == 32
        M[j] = max(M[j], p(w))

    def cardinality(self):
        m = self.m
        M = self.M

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