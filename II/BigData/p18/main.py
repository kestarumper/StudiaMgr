from os import listdir, path


def jaccard(set1, set2):
    nominator = float(len(set1.intersection(set2)))
    denominator = float(len(set1.union(set2)))
    return nominator / denominator


def to_shingles(line, k):
    tokens = line.split()
    return [tuple(tokens[i:i+k]) for i in range(len(tokens) - k + 1)]


k = 4
sets = []
paths = []
for fpath in [f for f in listdir("chapters") if path.isfile(path.join("chapters", f))]:
    current_set = set()
    with open("chapters/" + fpath, 'r') as file:
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
    jaccards[(c1, c2)] = '{:f}'.format(jaccard(s1, s2))

print(jaccards)
