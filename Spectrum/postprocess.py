#!/bin/env python


import sys
import numpy as np

A = np.loadtxt(sys.argv[1], delimiter=',')
print('Read in ', A.shape, ' matrix from ', sys.argv[1])

(m,n) = A.shape
D = np.zeros((m, n))
D[:,0] = A[:,0]
a1 = A[:,1]
for i in range(1,n):
    D[:,i] = A[:,i] - a1

np.savetxt(sys.argv[2], D, delimiter=',')
