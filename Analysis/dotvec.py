#!/usr/bin/env python
#
# Usage- dotvec.py model.pdb diffec.npy frequencies.asc modes.npy

import sys
import loos
import numpy as np

model = loos.createSystem(sys.argv[1])
subset = loos.selectAtoms(model, 'backbone && resid < 129')
#subset = loos.selectAtoms(model, 'backbone && (resid >= 42 && resid <= 79)')
indices = []
for atom in subset:
    indices.append(atom.id()-1)

dv = np.load(sys.argv[2])
dv = dv / np.linalg.norm(dv)
m = len(dv)

freqs = np.loadtxt(sys.argv[3])
n = len(freqs)

eigvecs = np.load(sys.argv[4])
U = eigvecs['arr_0']
Us = np.zeros( (m, n) )
k = 0
for j in indices:
    j3 = j*3
    Us[k, :] = U[j3, :]
    Us[k+1, :] = U[j3+1, :]
    Us[k+2, :] = U[j3+2, :]
    k += 3

for i in range(n):
    Us[:, i] /= np.linalg.norm(Us[:, i])


for j in range(len(freqs)):
    if freqs[j] < 1e-2:
        continue
    dp = np.dot(dv[:, 0], Us[:, j])
    print('{}\t{}'.format(freqs[j], abs(dp)))
    
