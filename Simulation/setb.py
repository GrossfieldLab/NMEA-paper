#!/bin/env python

import loos
import sys

model = loos.createSystem(sys.argv[1])
for atom in model:
    atom.bfactor(0.0)
subset = loos.selectAtoms(model, sys.argv[2])
for atom in subset:
    atom.bfactor(1.0)

pdb = loos.PDB.fromAtomicGroup(model)
print str(pdb)
