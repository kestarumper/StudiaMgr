from sympy import gcd, mod_inverse
import random
import itertools

random.seed(0)


def gen_privkey(n):
    sequence = []
    for i in range(n):
        if (random.randint(0, 1)):
            sequence.append(2 ** i)
    return sequence


def choose_W(M):
    while True:
        W = random.randint(2, M - 1)
        if gcd(W, M) == 1:
            return W


def gen_pubkey(A, W, M):
    """`b_i = Wa_i (mod M)`"""
    return [W * a % M for a in A]


def gen(n=128):
    A = gen_privkey(n)
    E = sum(A)
    M = random.randint(E+1, 2*E)
    W = choose_W(M)
    B = gen_pubkey(A, W, M)
    privkey = (A, W, M)
    return privkey, B


def string_to_binary(P):
    P = map(ord, list(P))
    P = map(lambda p: list(f"{p:08b}"), P)
    P = list(itertools.chain.from_iterable(P))
    return P


def to_groups(arr, n):
    return [arr[i:i+n] for i in range(0, len(arr), n)]


def binary_to_string(P):
    P = map(lambda x: ''.join(x), to_groups(P, 8))
    P = map(lambda x: int(x, base=2), P)
    P = filter(lambda x: x > 0, P)
    P = ''.join(list(map(chr, P)))
    return P


def enc(P, B):
    n = len(B)
    P = string_to_binary(P)
    P = to_groups(P, n)
    C = [sum([int(p) * b for p, b in zip(Pi, B)]) for Pi in P]
    return C


def easy_knapsack(s, A):
    result = []
    for a in reversed(A):
        if s >= a:
            s -= a
            result.append('1')
        else:
            result.append('0')
    if s != 0:
        raise Exception("s != 0")
    return list(reversed(result))


def dec(C, privkey):
    A, W, M = privkey
    w = mod_inverse(W, M)
    S = [w * c % M for c in C]
    P = list(itertools.chain.from_iterable([easy_knapsack(s, A) for s in S]))
    return str.rstrip(binary_to_string(P))
