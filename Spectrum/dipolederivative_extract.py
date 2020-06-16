#!/bin/env python

import sys

whole_data = []
input_file = open(sys.argv[1],'r')
outfile = open(sys.argv[2],'w')
for line in input_file:
	if line.startswith('  VIBRATION MODE'):
		freqline = line.split(' ') #split on whitespace
		freqwhole = freqline[5] #grab part of line w/ freq
		freq2 = line[32:44]
		freq = freqwhole[10:]
		outfile.write(freq2+', ')
	if line.startswith('  DIPOLE DERIVATIVES'):
		derivx = line[23:32]
		derivy = line[35:44]
		derivz = line[47:56]
		outfile.write(derivx+', '+derivy+', '+derivz)
		#outfile.write(derivx)
		outfile.write('\n')
       
