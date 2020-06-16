#!/bin/env python

import sys
import numpy as np
import math
import glob


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




spectra = []

if len(sys.argv) == 1:
    print('Usage- avganiso.py prefix scale file [file ...]')
    sys.exit(-1)

prefix = sys.argv[1]
scale = float(sys.argv[2])
filenames = sys.argv[3:]

print('Processing- ')
sys.stdout.flush()

counter = 0
expected_shape = None
for filename in filenames:
    if counter % 25 == 0:
        sys.stdout.write(str(counter))
    else:
        sys.stdout.write('.')
    sys.stdout.flush()
    counter += 1

#    print 'Reading from ', filename
    A = np.loadtxt(filename, delimiter=',')
    (m,n) = A.shape
    if expected_shape is None:
        expected_shape = A.shape
    elif expected_shape != A.shape:
        print("***WARNING: {} has shape {} and will be ignored.".format(filename, A.shape))
        continue
    D = np.zeros((m,n))
    D[:,0] = A[:,0]
    A *= scale
    a1 = A[:,1]
    for i in range (1,n):
        D[:,i] = A[:,i] - a1
    spectra.append(D)

print("Done")
print("Read in {} matrices.".format(len(spectra)))

(m,n) = spectra[0].shape
avg = np.zeros((m,n))
std = np.zeros((m,n))

for i in range(len(spectra)):
    avg += spectra[i]
avg /= (len(spectra))

for i in range(len(spectra)):
    D = spectra[i] - avg
    std += D*D

std /= (len(spectra)-1)
std = np.sqrt(std)

#avg *= scale
#std *= scale

avg[:,0] = spectra[0][:,0]
std[:,0] = spectra[0][:,0]

np.savetxt(prefix + '_avg.asc', avg)
np.savetxt(prefix + '_std.asc', std)

matrixToSplot(prefix + '_avg_plot.asc', avg)
matrixToSplot(prefix + '_std_plot.asc', std)

print('Done!')
