#!/bin/sh
# This is massive overkill -- 1000 vectors would have been plenty.

for i in 456 1536
do
    echo $i
    ./dot_dist.py $i 100000 50 ${i}_dim &
done
