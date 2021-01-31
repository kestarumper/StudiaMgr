from collections import Counter
import time
from memory_profiler import profile
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')


def lineToWords(line):
    return tokenizer.tokenize(line)


def fileToWords(file):
    while True:
        line = file.readline()
        if not line:
            break
        words = lineToWords(line)
        for word in words:
            if len(word) == 0:
                continue
            yield word


def misra_gries(stream, k):
    counter = Counter()

    for element in stream:
        if element in counter or len(counter) < k:
            counter[element] += 1
        else:
            for key in list(counter.keys()):
                counter[key] -= 1
                if counter[key] == 0:
                    del counter[key]
    return counter


@profile
def main():
    with open(f'../p1/lotr.txt', 'r') as file:
        start = time.process_time()
        stream = fileToWords(file)
        misra_gries(stream, 10)
        end = time.process_time() - start
        print(end)


main()
