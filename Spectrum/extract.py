#!/bin/env python

import sys
import loos
import loos.pyloos


def matchMetadata(structure, source):
    if len(structure) != len(source):
        print('Error- mismatch is system sizes.')
        sys.exit(-1)

    for i in range(len(structure)):
        structure[i].id( source[i].id() )
        structure[i].resid( source[i].resid() )
        structure[i].segid( source[i].segid() )


def alignWithBackbone(target, fiducial):
    tbb = loos.selectAtoms(target, 'backbone')
    fbb = loos.selectAtoms(fiducial, 'backbone')

    M = tbb.superposition(fbb)
    X = loos.XForm()
    X.load(M)
    target.applyTransform(X)


if len(sys.argv) != 6:
    print('Usage- extract.py PSF model traj fiducial frameno')
    sys.exit(-1)

hdr = ' '.join(sys.argv)

source_model = loos.createSystem(sys.argv[1])
model = loos.createSystem(sys.argv[2])
traj = loos.pyloos.Trajectory(sys.argv[3], model)
fiducial = loos.createSystem(sys.argv[4])
frameno = int(sys.argv[5])

frame = traj[frameno]
alignWithBackbone(frame, fiducial)
matchMetadata(frame, source_model)
pdb = loos.PDB.fromAtomicGroup(frame)
pdb.remarks().add(hdr)
print(str(pdb))

sys.exit(0)
