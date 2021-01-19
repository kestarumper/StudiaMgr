import numpy as np
from os import listdir, path


def to_shingles(line, k):
    tokens = line.split()
    return [tuple(tokens[i:i+k]) for i in range(len(tokens) - k + 1)]


def generate_random_hash_functions(seed, count):
    minint = np.iinfo(np.int64).min
    maxint = np.iinfo(np.int64).max

    masks = (np.random.RandomState(seed=seed)
             .randint(minint, maxint, count))

    hashes = np.empty(count, dtype=np.int64)
    hashes.fill(maxint)
    return masks, hashes


class MinHash(object):
    def __init__(self, H, seed=2137):
        self._H = H  # ile funkcji hashujących
        self._seed = seed
        self._masks, self._hashes = generate_random_hash_functions(seed, H)

    def jaccard(self, other):
        equal_indices = self._hashes == other._hashes
        equal_indices_sum = equal_indices.sum()
        hash_count = float(self._H)
        return equal_indices_sum / hash_count

    def add(self, v):
        self._hashes = np.minimum(
            self._hashes, np.bitwise_xor(self._masks, hash(v)))


for H in [50, 100, 250]:
    mh1 = MinHash(H)
    mh2 = MinHash(H)

    a = [1, 2, 3]
    b = [2, 3, 4]

    for el in a:
        mh1.add(el)

    for el in b:
        mh2.add(el)

    print(mh1.jaccard(mh2))

# {
# ('2 - Chapter 3. Three is Company.txt', '1 - Chapter 2.txt'):	0.009607
# ('5 - Chapter 6. Lothlurien.txt', '3 - Chapter 4. A Short Cut to Mushrooms.txt'):	0.007858
# ('3 - Chapter 4. A Short Cut to Mushrooms.txt', '2 - Chapter 3. Three is Company.txt'):	0.010047
# ('1 - Chapter 2.txt', '6 - Chapter 7. In the House of Tom Bombadil.txt'):	0.011066
# ('6 - Chapter 7. In the House of Tom Bombadil.txt', '4 - Chapter 5. A Conspiracy Unmasked.txt'):	0.012887
# }


H = 250
k = 3
sets = []
paths = []
for fpath in [f for f in listdir("../p18/chapters") if path.isfile(path.join("../p18/chapters", f))]:
    current_set = MinHash(H)
    with open("../p18/chapters/" + fpath, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            shingles = to_shingles(line, k)
            for shingle in shingles:
                current_set.add(shingle)
    sets.append(current_set)
    paths.append(fpath)


pairs = zip(sets[:-1], sets[1:])
chapter_pairs = zip(paths[:-1], paths[1:])

jaccards = {}
for (s1, s2), (c1, c2) in zip(pairs, chapter_pairs):
    jaccards[(c1, c2)] = '{:f}'.format(s1.jaccard(s2))

for (k, v) in jaccards.items():
    print("{}:\t{}".format(k, v))
