from pyspark import SparkContext, SparkConf
import numpy as np
from operator import add

conf = SparkConf().setAppName("p37").setMaster('local')
sc = SparkContext(conf=conf)


def gen_paths(pair):
    global neighbours
    u, adjacents = pair
    counted = 0
    for v1 in adjacents:
        for v2 in adjacents:
            if v1 < v2:
                adjacents_v1 = neighbours.get(v1)
                if adjacents_v1 != None and v2 in adjacents_v1:
                    counted += 1
    return (u, counted)


def get_triplets(p):
    u, triangles_count = p
    deg = len(neighbours[u])
    denominator = deg * (deg - 1.0) + 1
    return (u, 2 * triangles_count / denominator, deg)


def avg(a, b):
    count = (a[1] + b[1])
    return ((a[0] * a[1]) / count + (b[0] * b[1]) / count, count)


edges = sc.textFile(
    "../p36/web-Stanford.txt").map(lambda line: line.split()) \
    .map(lambda p: (int(p[0]), int(p[1]))) \
    .map(lambda p: p if p[0] < p[1] else (p[1], p[0])) \
    .distinct()

edgesGrouped = edges.groupByKey().mapValues(list)  # { u: N(u) }

neighbours = edgesGrouped.collectAsMap()

paths = edgesGrouped.map(lambda p: (p[0], p[1])).map(
    gen_paths)  # (u, #triangles)

reduced = paths.reduceByKey(add).map(get_triplets) # (u, cc, deg)

triangles = paths.map(lambda p: p[1]).reduce(add)
avgCC = reduced.map(lambda p: (p[1], 1)).reduce(avg)
avgDeg = reduced.map(lambda p: (p[2], 1)).reduce(avg)

print(reduced.collect())
print("Triangles ", triangles)
print("Avg CC", avgCC)
print("Avg Deg", avgDeg)

reduced.saveAsTextFile('coefficients.txt')

sc.stop()


# def countTriangles(p):
#     global neighbours
#     src, target = p[0]
#     u = p[1]
#     adjacents = neighbours.get(src)
#     if adjacents != None and target in adjacents:
#         return (u, 1)
#     else:
#         return (u, 0)
