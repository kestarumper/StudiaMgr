from pyspark import SparkContext, SparkConf
import numpy as np
from operator import add

conf = SparkConf().setAppName("Graph in out").setMaster('local')
sc = SparkContext(conf=conf)


def map_in_out(x):
    v = x[0]
    in_deg = next((y[1] for y in x[1] if y[0] == 'i'), 0)
    out_deg = next((y[1] for y in x[1] if y[0] == 'o'), 0)
    return (v, in_deg, out_deg)


def avg(a, b):
    count = (a[1] + b[1])
    return ((a[0] * a[1]) / count + (b[0] * b[1]) / count, count)

edges = sc.textFile(
    "web-Stanford.txt").map(lambda line: line.split())  # (u, v)
in_out_edges = edges.flatMap(
    lambda p: [((int(p[0]), 'o'), 1), ((int(p[1]), 'i'), 1)])  # ((u, 'o | i'), 1)
degrees = in_out_edges.reduceByKey(add).map(
    lambda p: (p[0][0], (p[0][1], p[1])))  # (u, ('o', n))
groupped = degrees.groupByKey().mapValues(list).sortByKey().map(map_in_out)

mappedIn = groupped.map(lambda p: (p[1], 1))
mappedOut = groupped.map(lambda p: (p[2], 1))
averageIn =  mappedIn.reduce(avg)[0]
averageOut =  mappedOut.reduce(avg)[0]

print(averageIn, averageOut)
print(groupped.take(10))

sc.stop()
