#!/bin/bash

echo "$0 $@" >launch_nma.command

PREFIX=${2:-ns}
PARTITION=${3:-preempt}
MEMORY="8gb"
TIMELIMIT="16:00:00"


if [ -z "$1" ] ; then
    echo "Usage- launch_nma.sh <array-spec> [prefix]"
    exit -1
fi


for d in run-0? ; do
    cd $d
    DIR=`pwd|cut -d/ -f5-6`
    TAG="$PREFIX:$DIR"
    sbatch --array="$1" -t $TIMELIMIT -p $PARTITION --mem=$MEMORY -c1 -n1  -J "$TAG" -o "$PREFIX-%A-%a.out" -e "$PREFIX-%A-%a.err" --constraint="E52680|E52680v3|E52690v2|E52695v2|E52695v4|E52697v4|E52699v4|E74809v3" ../process_frame.sh $PREFIX
    cd ..
done
