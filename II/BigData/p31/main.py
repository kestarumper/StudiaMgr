from pyspark import SparkContext, SparkConf
import numpy as np
from operator import add

conf = SparkConf().setAppName("Reverse graph").setMaster('local')
sc = SparkContext(conf=conf)

graph = [
    [1, [3, 4, 5]],
    [2, [1, 3]],
    [3, [4, 5]],
    [4, [1, 2]],
    [5, [4, 5]]
]

distData = sc.parallelize(graph)

edges_reversed = distData.flatMap(lambda x: map(lambda y: (y, x[0]), x[1]))
groupped = edges_reversed.groupByKey().mapValues(list)

print(groupped.collectAsMap())

sc.stop()
