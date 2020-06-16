#!/bin/bash

LOW=0
HIGH=300
NBINS=50

N=0
PREFIX=${1:-r10n6}
OUTPREF=${2:-r10n6}

for DIR in run-?? ; do
    echo "Processing $DIR..."
    cd $DIR
    rm freqs.asc

    if [ $N -eq 0 ] ; then
      N=$(ls -l ${PREFIX}-*/frame_f.asc | wc -l)
      echo "Using $N data points"
    fi
    flist=$(ls -l ${PREFIX}-*/frame_f.asc | head -n $N | gawk '{print $9}')
    cat $flist >freqs.asc
    histo.pl --norm=1 --bounds=$LOW,$HIGH --nbins=$NBINS --discard --col=0  freqs.asc >${OUTPREF}_vdos.asc 2>histo.log

    for d in ${PREFIX}-* ; do
	echo $DIR/$d
	cd $d
	histo.pl --norm=1 --bounds=$LOW,$HIGH --nbins=$NBINS --discard --col=0 frame_f.asc >${OUTPREF}_vdos.asc 2>histo.log
	cd ..
    done
    avgdata.pl --std ${PREFIX}-*/${OUTPREF}_vdos.asc >${OUTPREF}_vdos_avg.asc 2>>histo.log
    cd ..
done


avgdata.pl --std run-??/${OUTPREF}_vdos.asc >${OUTPREF}_avg_vdos.asc
avgdata.pl --std run-??/${OUTPREF}_vdos_avg.asc >${OUTPREF}_avg_vdos_avg.asc

    
