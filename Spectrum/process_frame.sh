#!/bin/bash

### Tod D. Romo
### Grossfield Lab, Biochemistry
### Center for Intergrated Research Computing
### University of Rochester

### Config
PREFIX=${1:ns}              # prefix for output directories and for tags
TOP=/path/to/project        # Top level (global halt file location)
SRUN=srun                   # command to use for srun


# Verify that we are part of a job array
if [ -z "$SLURM_ARRAY_TASK_ID" ] ; then
    echo "***ERROR***"
    echo "This job does not appear to be part of a job-array"
    exit -1
fi


# Look for local halt or global halt file
if [ -f halt -o -f $TOP/halt ] ; then
    exit -2
fi

INDEX=$SLURM_ARRAY_TASK_ID


# Record some info about where we are
hostname
grep 'model name' /proc/cpuinfo | sort | uniq

# Record the start time (for tracking total execution time)
echo "***STARTING***"
date

# Load required modules
module load impi/2018
module load loos
module load bzip2

# Force LOOS to only use 1 thread
export OPENBLAS_NUM_THREADS=1

# CHARMM is a local build, not a module
CHARMM=/path/to/charmm


# 0-pad the task id (6-digits)
PADDED_ID=`perl -e "printf'%06d',$SLURM_ARRAY_TASK_ID;"`
WORKDIR=$PREFIX-$PADDED_ID

if [ ! -d $WORKDIR ] ; then
    mkdir $WORKDIR
fi

cd $WORKDIR


#
# The following is designed for running in the preempt partition.  A job
# may be preempted at any time by the system.  If it is preempted, it will get
# re-queued.  I use the stage-NN files to indicate which step successfully completed
#

# Extract the frame
if [ ! -f stage-01 ] ; then
  $SRUN python ../../extract.py ../../charmmed.psf ../prod.pdb ../prod.dcd ../../fiducial.pdb $INDEX >frame.pdb
  touch stage-01
fi

# Select out a water shell and run the NMA
if [ ! -f stage-02 ] ; then
  cp ../../xtlvib.inp .
  $SRUN $CHARMM <xtlvib.inp >xtlvib.out
  touch stage-02
fi

# Extract the dipole derivatives
if [ ! -f stage-03 ] ; then
  $SRUN python ../../dipolederivative_extract.py xtlvib.out dipoles.csv
  touch stage-03
fi

# Calculate isotropic spectrum
if [ ! -f stage-04 ] ; then
  $SRUN python ../../IsotropicCalcHEWL2.py dipoles.csv iso.csv
  touch stage-04
fi

# Calculate anisotropic spectrum (single-threaded)
if [ ! -f stage-05 ] ; then
  $SRUN python ../../fastcalc.py dipoles.csv aniso.csv
  touch stage-05
fi

# Converts the CSV into an ascii matrix and subtracts off the 0-degree col
if [ ! -f stage-06 ] ; then
  $SRUN python ../../postprocess.py aniso.csv paniso.csv
  touch stage-06
fi

# Convert to splot format (for gnuplot)
if [ ! -f stage-07 ] ; then
  $SRUN perl ../../csv2splot.pl <paniso.csv >paniso.asc
  touch stage-07
fi

# Iso file is just the csv with the commas stripped...
if [ ! -f stage-08 ] ; then
  $SRUN sed 's/,/ /g' <iso.csv >iso.asc
  touch stage-08
fi

# Pull out the eigenvectors.  Makes frame_f (freqs), frame_s (eigvals), and
# frame_U (eigvecs).  The latter is a compressed numpy format file.
if [ ! -f stage-09 ] ; then
  $SRUN python ../../xeig.py xtlvib.out frame
  touch stage-09
fi

# Calculate collectivity
if [ ! -f stage-10 ] ; then
  $SRUN python ../../collectivity.py deleted.pdb all frame_U.npz >coll.asc
  touch stage-10
fi

# Compress the frame
if [ ! -f stage-11 ] ; then
  $SRUN bzip2 -v9 frame.pdb
  touch stage-11
fi

# Prune the CHARMm output since it's huge.
if [ ! -f stage-12 ] ; then
  $SRUN ../../prune_charmm_log.pl xtlvib.out >xtlvib_pruned.out
  $SRUN bzip2 -v9 xtlvib_pruned.out
  $SRUN rm xtlvib.out
  touch stage-12
fi

# Note the ending time for executing time tracking
echo "***ENDING***"
date

exit 0

