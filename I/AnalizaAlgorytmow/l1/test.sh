#!/bin/sh

ret=$(cargo build)

if [ "$?" = "0" ]
then
    n=1000
    u=1000

    ./target/debug/l1 --nodes $n --samples 10000 --scenario 2 > "n=$n-scenario=2.txt"

    udiv2=$(($u / 2)) 
    for n in 2 $udiv2 $u
    do
        ./target/debug/l1 --nodes $n --samples 10000 --scenario 3 --supremum $u > "n=$n-u=$u-scenario=3.txt"
    done
fi