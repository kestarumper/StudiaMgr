from merklehellman import gen, enc, dec

if __name__ == "__main__":
    (A, W, M), B = gen()
    P = "ala ma kota"
    C = enc(P, B)
    D = dec(C, (A, W, M))
    assert P == D, f"{P} != {D}"
