#!/bin/env python

import sys
import numpy as np
import re

## Compile search objects...

space_allocated_regexp = re.compile("Space allocated for\s+(\d+) vectors of length\s+(\d+)")
vibration_regexp = re.compile("VIBRATION MODE\s*(\d+)\s*FREQUENCY=\s*([0-9.Ee-]+)")
eigenvalue_regexp = re.compile("EIGENVALUE=\s*([0-9.eE-]+)")
eigenvector_regexp = re.compile("EIGENVECTOR:")
polarizability_regexp = re.compile("TOTAL POLARIZABILITY")



logfile = sys.argv[1]
prefix = sys.argv[2]

print('Processing...')
f = open(logfile)
index = -1
state = 0
j = 0

for line in f:
    if state == 0:
        m = space_allocated_regexp.search(line)
        if m:
            nmodes = int(m.group(1))
            nelems = int(m.group(2))
            if nelems % 3 != 0:
                print('Error- found {} elements per eigenvector, but must be a multiple of 3!'.format(nelems))
                sys.exit(-1)
            natoms = nelems / 3

            print('Input has {} atoms and {} modes'.format( natoms, nmodes ))

            eigvals = np.zeros( (nmodes, 1) )
            frequencies = np.zeros( (nmodes, 1) )
            eigvecs = np.zeros( (nelems, nmodes) )

            state = 1

    elif state == 1:
        m = vibration_regexp.search(line)
        if m:
            index = int(m.group(1)) - 1
            frequencies[index] = float(m.group(2))
        else:
            m = eigenvalue_regexp.search(line)
            if m:
                eigvals[index] = float(m.group(1))
            else:
                if eigenvector_regexp.search(line):
                    state = 2
                    j = 0
    elif state == 2:
        line = line.rstrip('\n\r')
        if line == '' or polarizability_regexp.search(line):
            state = 1
        else:
            ary = line.split()
            eigvecs[j, index] = float(ary[4])
            eigvecs[j+1, index] = float(ary[5])
            eigvecs[j+2, index] = float(ary[6])
            j += 3


print('Saving...')
np.savetxt(prefix + '_f.asc', frequencies)
np.savetxt(prefix + '_s.asc', eigvals)
np.savez_compressed(prefix + '_U' , eigvecs)

print('Done!')
