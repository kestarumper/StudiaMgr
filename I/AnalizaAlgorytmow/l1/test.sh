#!/bin/sh

ret=$(cargo build)

if [ "$?" = "0" ]
then
    for n in 100 1000
    do
        ./target/debug/l1 --nodes $n --samples 10000 --scenario 2 > "n=$n-scenario=2.txt"
    done

    for u in 100 1000
    do
        udiv2=$(($u / 2)) 
        for n in 2 $udiv2 $u
        do
            ./target/debug/l1 --nodes $n --samples 10000 --scenario 3 --supremum $u > "n=$n-u=$u-scenario=3.txt"
        done
    done
fi