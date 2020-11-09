from pyspark import SparkContext, SparkConf
import numpy as np
from operator import add

conf = SparkConf().setAppName("Stats").setMaster('local')
sc = SparkContext(conf=conf)


def mean(x, y):
    (a, m) = x
    (b, n) = y
    N = m + n
    return (((a * m) / N) + ((b * n) / N), N)


data = np.random.randint(0, 2_000_000, size=1_000_000)
distData = sc.parallelize(data)

gmin = distData.reduce(min)
gmax = distData.reduce(max)
N = distData.count()
avg = distData.map(lambda x: (x, 1)).reduce(mean)[0]
distinct = distData.distinct()
numOfElements = distData \
    .map(lambda x: (x, 1)) \
    .reduceByKey(add) \
    .filter(lambda y: y[1] == 1) \
    .count()

geometricMean = distData.reduce(lambda a, b: a ** (1./N) * b ** (1./N))
harmonicMean = N / distData.map(lambda x: 1/x).sum()

print({"min": gmin, "max": gmax, "n": N, "avg": avg,
       "G": geometricMean, "H": harmonicMean})
print(np.mean(data))
print(distinct.take(100))
print(numOfElements)

sc.stop()
