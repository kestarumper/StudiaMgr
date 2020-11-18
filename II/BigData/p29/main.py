from pyspark import SparkContext, SparkConf
import numpy as np
from operator import add

conf = SparkConf().setAppName("Stats").setMaster('local')
sc = SparkContext(conf=conf)

def seq_operator(acc, value):
    min_v, max_v, count, avg_v, distinct = acc

    count += 1

    min_v = min(min_v, value)
    max_v = max(max_v, value)

    avg_v = ((count - 1) / count) * avg_v + (value / count)

    if not distinct.get(value):
        distinct[value] = True
    
    return (min_v, max_v, count, avg_v, distinct)

def comb_operator(x, y):
    min_v = min(x[0], y[0])
    max_v = max(x[1], y[1])
    count = x[2] + y[2]
    avg_v = (x[2] / count) * x[3] + (y[2] / count) * y[3]
    distinct = {**x[4], **y[4]}
    return (min_v, max_v, count, avg_v, distinct)

data = np.random.randint(0, 10_000_000, size=1_000_000)
distData = sc.parallelize(data)

labels = ["min", "max", "count", "avg", "distinct", "distinct_num"]
zero_value = (data[0], data[0], 0, 0, {})

result = distData.aggregate(zero_value, seq_operator, comb_operator)
result = result[:-1] + (len(result[-1]),)

verbose = zip(labels, result)

print({ k: v for k, v in verbose })

sc.stop()
