#!/bin/bash

P=/path/to/difference/vectors


DIR=`pwd`
X=$DIR/dv.asc

rm $X

for d in run-??/r10n6-* ; do
    echo $d
    pushd $d >/dev/null 2>&1
    $P/dotvec.py deleted.pdb $P/c2i_full.npy frame_f.asc frame_U.npz >dv.asc
#    $P/dotvec.py deleted.pdb $P/c2i_42-79.npy frame_f.asc frame_U.npz >dvs.asc
    cat dv.asc >>$X
    popd >/dev/null 2>&1
done
