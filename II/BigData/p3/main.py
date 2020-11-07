from pyspark import SparkContext, SparkConf
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import csv

tokenizer = RegexpTokenizer(r'\w+')
fname = "lotr.txt"
conf = SparkConf().setAppName("Book").setMaster('local')
sc = SparkContext(conf=conf)

def lineToWords(line):
    return tokenizer.tokenize(line)

def filterStopWords(word):
    return (word not in stopWords) and (len(word) > 0)

def writeCSVToFile(data, fname):
    with open(fname,'w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['weight','word'])
        csv_out.writerows(data)

stopWords = stopwords.words("english")

lines = sc.textFile(fname)
words = lines.flatMap(lineToWords)
filtered = words.filter(filterStopWords)
pairs = filtered.map(lambda w: (w.lower(), 1))
grouped = pairs.reduceByKey(lambda a, b: a + b)
sorted = grouped.sortBy(lambda x: -x[1])

writeCSVToFile(sorted.map(lambda x: (x[1], x[0])).take(500), "wordcloud.csv")

sc.stop()
