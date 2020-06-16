#!/usr/bin/env python

import sys
import loos
import numpy as np

left = loos.createSystem(sys.argv[2])
right = loos.createSystem(sys.argv[3])

left_bb = loos.selectAtoms(left, 'backbone && resid < 129')
right_bb = loos.selectAtoms(right, 'backbone && resid < 129')

nl = len(left_bb)
nr = len(right_bb)

if nl != nr:
    print('***ERROR: systems have wrong size')
    print("Left has size {}, but right has size {}".format(nl, nr))
    print("Left:")
    print(str(loos.PDB.fromAtomicGroup(left_bb)))
    print("Right:")
    print(str(loos.PDB.fromAtomicGroup(right_bb)))
    
    sys.exit(-1)

D = np.zeros( (nl*3, 1) )

k = 0
for i in range(nl):
    d = left_bb[i].coords() - right_bb[i].coords()
    D[k, 0] = d[0]
    D[k+1, 0] = d[1]
    D[k+2, 0] = d[2]

    k += 3

np.save(sys.argv[1], D)
