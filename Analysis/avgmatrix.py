#!/bin/env python

import sys
import numpy as np
import math

use_standard_error = True

def matrixToSplot(fname, A, factor=15.0):
    (m, n) = A.shape
    fout = open(fname, 'w')
    for j in range(m):
        frequency = A[j][0]
        for i in range(1, n):
            line = "%f\t%f\t%f\n" % ( ((i-1)*factor), frequency, A[j][i])
            fout.write(line)
        fout.write('\n')
    fout.close()




prefix = sys.argv[1]
filenames = sys.argv[2:]

matrices = []
for filename in filenames:
    A = np.loadtxt(filename)
    matrices.append(A)

avg = np.mean(matrices, axis=0)
std = np.std(matrices, axis=0)
if use_standard_error:
    std /= math.sqrt(len(matrices))
std[:,0] = avg[:,0]

np.savetxt(prefix + '_avg.asc', avg)
matrixToSplot(prefix + '_avg_plot.asc', avg)

np.savetxt(prefix + '_std.asc', std)
matrixToSplot(prefix + '_std_plot.asc', std)
