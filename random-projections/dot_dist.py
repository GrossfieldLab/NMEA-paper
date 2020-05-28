#!/usr/bin/env python3

import sys
import numpy
import hypersphere

num_dim = int(sys.argv[1])
num_vectors = int(sys.argv[2])
num_bins = int(sys.argv[3])
outfile = sys.argv[4]

bin_width = 1. / num_bins

hist = numpy.zeros(num_bins)

vector_generator = hypersphere.HyperSphere(num_dim)

vectors = []

for i in range(num_vectors):
    vectors.append(vector_generator.vector())

for i in range(num_vectors-1):
    for j in range(i+1, num_vectors):
        d = abs(numpy.add.reduce(vectors[i] * vectors[j]))
        bin = int(d // bin_width)
        hist[bin] += 1

num_points = numpy.add.reduce(hist)
hist /= num_points
cum = numpy.add.accumulate(hist)

bin_centers = numpy.arange(0., 1.0, bin_width)
bin_centers += 0.5 * bin_width

hist_name = outfile + '.hist'
hist = numpy.vstack([bin_centers, hist]).T
numpy.savetxt(hist_name, hist, header='n_dim = ' + str(num_dim) + 'n_points = ' + str(num_points))

cum_name = outfile + '.cum'
cum = numpy.vstack([bin_centers, cum]).T
numpy.savetxt(cum_name, cum, header='n_dim = ' + str(num_dim) + 'n_points = ' + str(num_points))
