from hll import hash_fn_factory, HyperLogLog


def main():
    b = 8
    hyperll_src = HyperLogLog('sha256', b)
    hyperll_dest = HyperLogLog('sha256', b)
    hyperll_pair = HyperLogLog('sha256', b)
    hyperll_pair2 = HyperLogLog('sha256', b)

    i = 0
    with open("lbl-pkt-4.tcp", 'r') as file:
        line = file.readline()
        while line:
            data = line.split()
            [_, src, dest, _, _, _] = data

            pair = src + "_" + dest if src < dest else dest + "_" + src
            pair2 = src + "_" + dest
            print(i, src, dest, pair, pair2, end="\r", flush=True)

            hyperll_src.add(src)
            hyperll_dest.add(dest)
            hyperll_pair.add(pair)
            hyperll_pair2.add(pair2)

            line = file.readline()
            i += 1

    print("\r\nSrc:\t", hyperll_src.cardinality())
    print("Dest:\t", hyperll_dest.cardinality())
    print("Pair:\t", hyperll_pair.cardinality())
    print("Pair2:\t", hyperll_pair2.cardinality())


if __name__ == "__main__":
    main()
