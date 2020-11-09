from pyspark import SparkContext, SparkConf
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import csv
from operator import add

tokenizer = RegexpTokenizer(r'\w+')
fname = "lotr.txt"
conf = SparkConf().setAppName("Book").setMaster('local')
sc = SparkContext(conf=conf)

stopWords = stopwords.words("english")


def lineToWords(line):
    words = list(filter(lambda w: w not in stopWords,
                        tokenizer.tokenize(line.lower())))
    pairs = zip(words[:-1], words[1:])
    return pairs


def topFive(words):
    words = list(words)
    wordDict = dict.fromkeys(words, 0)
    for word in words:
        wordDict[word] += 1
    return list(map(lambda x: x[0], sorted(wordDict.items(), key=lambda x: x[1], reverse=True)[:5]))


def writeCSVToFile(data, fname):
    with open(fname, 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['weight', 'word'])
        csv_out.writerows(data)


lines = sc.textFile(fname)
pairs = lines.flatMap(lineToWords)
grouped = pairs.groupByKey().mapValues(topFive)

print(grouped.sample(False, 0.001).collect())

sc.stop()
