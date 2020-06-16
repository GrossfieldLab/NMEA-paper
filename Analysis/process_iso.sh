#!/bin/bash
#
# Add frequencies to ISO file and perform a binned average within runs,
# then get the overall average.
#


PREFIX=${1:-r10n6}
OUTPREF=${2:-r10n6}

# First, need to add the frequencies back in...
for RUN in run-* ; do
    cd $RUN
    echo "+ $RUN"
    ../avgdata.pl --std ${PREFIX}-*/iso.asc >${OUTPREF}_iso_avg.asc
  cd ..
done

./avgdata.pl --std run-??/${OUTPREF}_iso_avg.asc >${OUTPREF}_avg_iso_avg.asc


