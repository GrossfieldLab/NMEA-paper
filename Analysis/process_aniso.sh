#!/bin/bash
#

SCALE="1e6"

PREFIX=${1:-r10n6}

for RUN in run-?? ; do
  cd $RUN
  echo $RUN
  python ../avganiso.py ${PREFIX}_avganiso $SCALE ${1:-ss}-*/aniso.csv
  cd ..
done

python ./avgmatrix.py ${PREFIX}_avganiso run-??/${PREFIX}_avganiso_avg.asc
