from pyspark import SparkContext, SparkConf
import numpy as np
from operator import add

conf = SparkConf().setAppName("Graph in out").setMaster('local')
sc = SparkContext(conf=conf)

edges = sc.textFile(
    "../p36/web-Stanford.txt").map(lambda line: line.split()) \
    .map(lambda p: (int(p[0]), int(p[1]))) \
    .map(lambda p: p if p[0] < p[1] else (p[1], p[0])) \
    .groupByKey() \
    .mapValues(lambda x: list(set(x))) \
    .mapValues(len)

print(edges.take(10))

sc.stop()
