from pyspark import SparkContext, SparkConf
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import csv
from operator import add
import random

tokenizer = RegexpTokenizer(r'\w+')
fname = "lotr.txt"
conf = SparkConf().setAppName("Book").setMaster('local')
sc = SparkContext(conf=conf)

stopWords = stopwords.words("english")


def lineToWords(line):
    words = tokenizer.tokenize(line.lower())
    pairs = zip(words[:-1], words[1:])
    return pairs


def filterStopWords(pair):
    return (pair[0] not in stopWords) and (pair[1] not in stopWords)


def topFive(words):
    words = list(words)
    wordDict = dict.fromkeys(words, 0)
    for word in words:
        wordDict[word] += 1
    return list(map(lambda x: x[0], sorted(wordDict.items(), key=lambda x: x[1], reverse=True)[:5]))


def paragraph(words, n):
    result = []
    word, next5 = random.sample(words.items(), 1)[0]
    result.append(word)
    for _ in range(n):
        try:
            nextWord = random.sample(next5, 1)[0]
            result.append(nextWord)
            nextOfNext = words[nextWord]
            next5 = nextOfNext
            pass
        except:
            pass
    return ' '.join(result)


lines = sc.textFile(fname)
pairs = lines.flatMap(lineToWords).filter(
    filterStopWords).map(lambda p: (p, 1))
reduced = pairs.reduceByKey(add).sortBy(
    lambda p: p[1]).map(lambda p: (p[0][0], p[0][1]))
grouped = reduced.groupByKey().mapValues(topFive)

mapped = grouped.collectAsMap()
# print(mapped)
print("\n\n")
print(paragraph(mapped, 100))

print("\n\n")
print(paragraph(mapped, 100))

print("\n\n")
print(paragraph(mapped, 100))

sc.stop()
