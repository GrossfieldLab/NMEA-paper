#!/bin/bash

LOW=0
HIGH=250
NBINS=100

PREFIX=${1:-ss}


for DIR in run-?? ; do
    cd $DIR
    echo "+ $DIR"

    for d in $PREFIX-* ; do
        cd $d
#	echo "- $DIR:$d"
	if [ ! -f fcoll.asc ] ; then
            ../../../add_freq_to_coll.pl frame_f.asc coll.asc >fcoll.asc || exit -1
	fi
        cd ..
    done
    ../../binnedavg.pl $LOW $HIGH $NBINS $PREFIX-*/fcoll.asc >avgcoll.asc || exit -1
    cd ..
done

../avgdata.pl --std run-??/avgcoll.asc >avgcoll.asc
