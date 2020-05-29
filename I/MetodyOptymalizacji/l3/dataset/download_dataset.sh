#!/bin/bash
url=https://raw.githubusercontent.com/brzepkowski/workspace/master/Metody%20Optymalizacji/Lista%203/
for i in {1..12}
do
  fname="gap${i}.txt"
  curl "${url}${fname}" > $fname
done
for i in {a..d}
do
  fname="gap${i}.txt"
  curl "${url}${fname}" > $fname
done
